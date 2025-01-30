from typing import List, Optional
from dataclasses import dataclass
import datetime
from io import BytesIO

# from common.utils import datetime_util
# from sales_crm_core.adapters.iam_service import IamService
# from sales_crm_core.adapters.service_adapter import get_service_adapter
from convert_html_to_pdf import HTMLToPDFConverter
from pdf_flowable_blocks.pdf_flowable_blocks.remarks_block import ExtraFeatureParagraph
from pdf_flowable_blocks.pdf_flowable_blocks.header_block import HeaderBlockV2
from reportlab.platypus import SimpleDocTemplate, Spacer
from reportlab.lib.pagesizes import letter

@dataclass
class PipelineItemRemarkAddedAtDTO:
    pipeline_item_remarks_id: str
    pipeline_item_id: str
    added_at: datetime.datetime
@dataclass
class PipelineItemRemarksDTO(PipelineItemRemarkAddedAtDTO):
    remarks: Optional[str]
    added_by: str
    last_updated_at: Optional[datetime.datetime]
    task_reference_id: Optional[str]
    pipeline_id: Optional[str]
    is_drafted_remarks: Optional[bool]

REMARKS = [
            {
               "pipelineItemRemarksId":"14c70a1d-3990-4d92-b32f-521d92a70db5",
               "pipelineItemId":"23645e99-d590-406c-8b30-d78ecea065a3",
               "remarks":"<p>Normal Text. Normal Text Normal Text Normal Text Normal Text Normal Text Normal Text Normal TextNormal Text</p><p><br></p><p><strong>Bold Text Bold Text Bold Text Bold Text Bold Text </strong></p><p><br></p><p><em>Italic Text Italic Text Italic Text Italic Text Italic Text </em></p><p><br></p><p><u>Underline Text Underline Text Underline Text Underline Text Underline Text Underline Text Underline Text </u></p><p><br></p><p><br></p><p><a href=\"https://bps-officer-alpha.flowwlabs.tech/templates/c0f628ce-1b12-47d9-b1ba-7069e864231c/b/15cd7e47-f0af-4550-9a0f-ef8fb0e6c910?pid=271e916b-1bd5-4964-8eeb-0dcc608567bb&amp;rid=23645e99-d590-406c-8b30-d78ecea065a3\" rel=\"noopener noreferrer\" target=\"_blank\">Hyper Link Hyper Link Hyper Link Hyper Link Hyper Link Hyper Link Hyper Link </a></p><p><br></p><p><br></p><ol><li>Bullet 1</li><li>Bullet 1</li><li>Bullet 1</li><li>Bullet 1</li><li>Bullet 1</li></ol><p><br></p><p><br></p><ul><li>Ordered 1</li><li>Ordered 2</li><li>Ordered 1</li><li>Ordered 1</li><li>Ordered 1</li><li>Ordered 1</li></ul><p><br></p><p class=\"ql-align-center\">Middle Text</p><p class=\"ql-align-center\">Middle TextMiddle TextMiddle TextMiddle Text</p><p class=\"ql-align-center\">Middle TextMiddle TextMiddle Text</p><p class=\"ql-align-center\"><br></p><p class=\"ql-align-right\">Middle TextMiddle Text</p><p class=\"ql-align-right\"><br></p><p class=\"ql-align-right\">Right Text</p>",
               "addedAt":"2025-01-27 21:30:21",
               "lastUpdatedAt":"2025-01-27 21:30:21",
               "addedBy":{
                  "userId":"2e3b0eec-0fe2-4e98-9259-d66060069b78",
                  "name":"Sankar",
                  "profilePicUrl":"",
                  "isActive":True,
                  "attendance":None,
                  "__typename":"BaseUser"
               },
               "attachments":[

               ],
               "__typename":"PipelineItemRemarks"
            },
            {
               "pipelineItemRemarksId":"c745a9ff-0fc5-4632-9097-8893000bfa04",
               "pipelineItemId":"23645e99-d590-406c-8b30-d78ecea065a3",
               "remarks":"<p>Random Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random TextRandom Text. Random Text</p>",
               "addedAt":"2025-01-27 20:53:16",
               "lastUpdatedAt":"2025-01-27 20:53:16",
               "addedBy":{
                  "userId":"2e3b0eec-0fe2-4e98-9259-d66060069b78",
                  "name":"Sankar",
                  "profilePicUrl":"",
                  "isActive":True,
                  "attendance":None,
                  "__typename":"BaseUser"
               },
               "attachments":[

               ],
               "__typename":"PipelineItemRemarks"
            },
            {
               "pipelineItemRemarksId":"33f1da91-3fa6-43a0-a361-16f4d24806a9",
               "pipelineItemId":"23645e99-d590-406c-8b30-d78ecea065a3",
               "remarks":"<p>Normal Text</p><p>Bold Text</p><p>Italic Text</p><p>Underline Text</p><p><a href=\"https://bps-officer-alpha.flowwlabs.tech/templates/c0f628ce-1b12-47d9-b1ba-7069e864231c/b/15cd7e47-f0af-4550-9a0f-ef8fb0e6c910?pid=271e916b-1bd5-4964-8eeb-0dcc608567bb&amp;rid=23645e99-d590-406c-8b30-d78ecea065a3\" rel=\"noopener noreferrer\" target=\"_blank\">Hyper Link</a></p><p><br></p><ol><li>List 1</li><li>List 2</li><li>List 3</li></ol><p><br></p><ul><li>List 1</li><li>List 2</li><li>List 3</li></ul><p><br></p><p class=\"ql-align-center\">sdfksdklfjsd</p><p class=\"ql-align-center\">sdfl;kajsd;fklasdf</p><p class=\"ql-align-center\">ssdfl;kasjd;flskdfjsd</p><p class=\"ql-align-center\">Middle Text</p><p class=\"ql-align-center\"><br></p><p class=\"ql-align-center\"><br></p><p class=\"ql-align-right\">Right Text</p><p class=\"ql-align-right\">Right Text 2</p>",
               "addedAt":"2025-01-27 18:44:28",
               "lastUpdatedAt":"2025-01-27 18:44:28",
               "addedBy":{
                  "userId":"2e3b0eec-0fe2-4e98-9259-d66060069b78",
                  "name":"Sankar",
                  "profilePicUrl":"",
                  "isActive":True,
                  "attendance":None,
                  "__typename":"BaseUser"
               },
               "attachments":[

               ],
               "__typename":"PipelineItemRemarks"
            },
            {
               "pipelineItemRemarksId":"acb5cf3e-ae2c-4d44-901b-898c5e6f7378",
               "pipelineItemId":"23645e99-d590-406c-8b30-d78ecea065a3",
               "remarks":"<p>Hi we have some text here</p>",
               "addedAt":"2025-01-27 18:17:05",
               "lastUpdatedAt":"2025-01-27 18:17:05",
               "addedBy":{
                  "userId":"2e3b0eec-0fe2-4e98-9259-d66060069b78",
                  "name":"Sankar",
                  "profilePicUrl":"",
                  "isActive":True,
                  "attendance":None,
                  "__typename":"BaseUser"
               },
               "attachments":[

               ],
               "__typename":"PipelineItemRemarks"
            }
         ]

class ConvertRemarksToPDFInteractor:
    def convert_remarks_to_pdf(self):
        # user_ids = [dto.added_by for dto in remark_dtos]
        # user_dtos, _ = self.iam_service.get_user_profiles(user_ids=user_ids)
        # user_name_map = {dto.user_id: dto.name for dto in user_dtos}

        html_content = ""
        flowables = []

        header_block = HeaderBlockV2()
        header = header_block.create_header_flowables(logo_url="https://crm-backend-media-static.s3.ap-south-1.amazonaws.com/alpha/media/tgbpass_logo.png",
                     header_text="HYDERABAD METROPOLITAN DEVELOPMENT AUTHORITY",
                    sub_header_text="TOWN PLANNING SECTION", sub_sub_header_text="NOTESHEET REPORT",
                    right_block_text="BuildNow")
        flowables.extend(header)
        for remark_dto in REMARKS:
            added_by = remark_dto["addedBy"]["name"]

            # user_name = user_name_map[added_by]

            added_at = remark_dto["addedAt"]
            remarks = remark_dto["remarks"]
            curr_html_content = f"""
            <p><b>{added_by}</b>:- {added_at}</p>
            {remarks}
            <br></br>
            <br></br>
            """
            header_right_text = added_by
            header_left_text = added_at

            extra_paragraph = ExtraFeatureParagraph()
            header_flowable = extra_paragraph.create_feature_paragraph_flowables(
                header_right_text = header_right_text, header_left_text = header_left_text)
            flowables.extend(header_flowable)

            html_content += curr_html_content
            htmltopdf = HTMLToPDFConverter()
            remarks = htmltopdf.convert(remarks)
            flowables.extend(remarks)

            flowables.append(Spacer(1, 12))

        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=72,
            leftMargin=50,
            topMargin=72,
            bottomMargin=72,
        )
        doc.build(flowables)
        pdf_bytes = buffer.getvalue()
        buffer.close()

        return pdf_bytes
