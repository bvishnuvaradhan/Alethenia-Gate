"""Rectification state — triggered when truth score < 70."""
from __future__ import annotations
from pydantic import BaseModel
from .base import State


class RectClaim(BaseModel):
    original:  str = ""
    rectified: str = ""
    action:    str = "kept"   # kept | corrected | removed
    reason:    str = ""


class RectState(State):
    rectifying:      bool = False
    rect_done:       bool = False
    rect_text:       str  = ""
    rect_score:      int  = 0
    rect_claims:     list[RectClaim] = []
    rect_models_used: int = 0

    # The original stream text — set by IntState after streaming
    original_stream: str = ""

    async def run_rectify(self):
        """Called when truth score < 70 after interrogation."""
        if not self.original_stream.strip():
            return

        self.rectifying  = True
        self.rect_done   = False
        self.rect_text   = ""
        self.rect_claims = []
        self.status_msg  = "Running rectification pipeline..."
        yield

        try:
            from ..backend.rectifier import rectify
            result = await rectify(
                original_prompt=self.stream if hasattr(self, "prompt") else "query",
                primary_response=self.original_stream,
                current_score=self.truth_score,
            )

            self.rect_text   = result.rectified_text
            self.rect_score  = result.new_score
            self.rect_claims = [
                RectClaim(
                    original=c.original,
                    rectified=c.rectified,
                    action=c.action,
                    reason=c.reason,
                )
                for c in result.claims
            ]
            self.rect_models_used = result.models_agreed
            self.rect_done   = True

        except Exception as e:
            self.rect_done  = True
            self.rect_text  = self.original_stream
            self.rect_score = self.truth_score
            self.status_msg = f"Rectification error: {e}"
            yield
            import asyncio
            await asyncio.sleep(3)
            self.status_msg = ""
            yield
            return

        self.rectifying = False
        self.status_msg = "Rectification complete."
        yield
        import asyncio
        await asyncio.sleep(2)
        self.status_msg = ""
        yield

    def dismiss_rect(self):
        self.rect_done   = False
        self.rect_text   = ""
        self.rect_claims = []
        self.rect_score  = 0
