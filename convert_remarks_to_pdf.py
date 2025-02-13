from io import BytesIO
from typing import List, Optional
from dataclasses import dataclass
from reportlab.platypus import SimpleDocTemplate, Spacer, Paragraph
import datetime
from reportlab.lib.styles import ParagraphStyle

from pdf_letter_generator.pdf_blocks.pdf_config import PDFConfig
from pdf_flowable_blocks.pdf_flowable_blocks.remarks_header_block import (
    RemarksHeaderBlock,
)
from pdf_flowable_blocks.pdf_flowable_blocks.remark_block import (
    RemarkBlock,
)
from convert_html_to_pdf import HTMLToPDFConverter


@dataclass
class PipelineItemRemarkAddedAtDTO:
    pipeline_item_remarks_id: str
    pipeline_item_id: str
    added_at: datetime.datetime


@dataclass
class PipelineItemRemarksDTO(PipelineItemRemarkAddedAtDTO):
    remarks: Optional[str]
    added_by: str
    designation: str
    last_updated_at: Optional[datetime.datetime]
    task_reference_id: Optional[str]
    pipeline_id: Optional[str]
    is_drafted_remarks: Optional[bool]

@dataclass
class RemarkDTO:
    added_by: str
    added_at: datetime.datetime
    remarks: str


class ConvertRemarksToPDFInteractor:
    # @property
    # def iam_service(self) -> IamService:
    #     return get_service_adapter().iam_service

    def convert_remarks_to_pdf(
        self, remark_dtos: List[PipelineItemRemarksDTO],
            extra_remark_dto: Optional[RemarkDTO] = None
    ):
        # user_ids = [dto.added_by for dto in remark_dtos]
        # user_dtos, _ = self.iam_service.get_user_profiles(user_ids=user_ids)
        # user_name_map = {dto.user_id: dto.name for dto in user_dtos}

        flowables = []

        remarks_header_block = RemarksHeaderBlock()
        header = remarks_header_block.create_remarks_header_flowables(
            logo_url="https://crm-backend-media-static.s3.ap-south-1.amazonaws.com/alpha/media/tgbpass_logo.png",
            header_text="HYDERABAD METROPOLITAN DEVELOPMENT AUTHORITY",
            sub_header_text="TOWN PLANNING SECTION",
            sub_sub_header_text="NOTESHEET REPORT",
            right_block_text="BuildNow",
        )
        flowables.extend(header)
        for remark_dto in remark_dtos:
            added_by = remark_dto.added_by
            user_name = "Sankar"
            designation = "Planning Ofcr"

            user = f"<b>{user_name}</b> [{designation}]"

            added_at = remark_dto.added_at
            formatted_date = f"<b><i>{added_at.strftime('%d %B %Y %I:%M:%S %p')}</i></b>"

            header_right_text = user
            header_left_text = formatted_date

            remarks_block = RemarkBlock()
            header_flowable = remarks_block.create_remark_flowables(
                header_right_text=header_right_text,
                header_left_text=header_left_text,
            )
            flowables.extend(header_flowable)

            htmltopdf = HTMLToPDFConverter()
            remark_stories = htmltopdf.convert_html_content_to_stories(
                html_content=remark_dto.remarks
            )
            flowables.extend(remark_stories)

            flowables.append(Spacer(1, 12))

        if extra_remark_dto:
            user_name = extra_remark_dto.added_by
            designation = "Planning Ofcr"

            user = f"<b>{user_name}</b> [{designation}]"

            added_at = extra_remark_dto.added_at
            formatted_date = f"<b><i>{added_at.strftime('%d %B %Y %I:%M:%S %p')}</i></b>"

            header_right_text = user
            header_left_text = formatted_date

            remarks_block = RemarkBlock()
            header_flowable = remarks_block.create_remark_flowables(
                header_right_text=header_right_text,
                header_left_text=header_left_text,
            )
            flowables.extend(header_flowable)

            remarks = Paragraph(extra_remark_dto.remarks,
                                style=ParagraphStyle(name="remarks", fontName="Helvetica", fontSize=12,
                                                     leading=15))
            flowables.append(remarks)



        buffer = BytesIO()

        # pdf_watermark_image_url = WATERMARK_IMAGE_URL
        # def add_watermark(canvas, doc):
        #     if pdf_watermark_image_url:
        #         from plugins.interactors.dms.pdf_blocks.watermark_block import (
        #             add_centered_watermark,
        #         )
        #
        #         add_centered_watermark(
        #             canvas, pdf_watermark_image_url, opacity=0.1, scale=1
        #         )

        doc = SimpleDocTemplate(
            buffer,
            pagesize=PDFConfig.PAGE_SIZE,
            leftMargin=PDFConfig.MARGIN,
            rightMargin=PDFConfig.MARGIN,
            topMargin=PDFConfig.MARGIN,
            bottomMargin=PDFConfig.MARGIN,
        )
        doc.build(flowables)
        pdf_bytes = buffer.getvalue()
        buffer.close()

        return pdf_bytes
