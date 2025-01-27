from io import BytesIO
from typing import Any, List

from reportlab.pdfgen import canvas
from reportlab.platypus import Flowable, SimpleDocTemplate

from plugins.constants.dms_enums import PDFBlockType
from plugins.interactors.dms.pdf_blocks import dtos
from plugins.interactors.dms.pdf_blocks.pdf_config import PDFConfig


class GeneratePDFWithFlowablesInteractor:
    def generate_pdf(
        self,
        pdf_block_dtos: List[dtos.PDF_BLOCK_UNION_TYPE],
        pdf_watermark_image_url: str,
    ) -> bytes:
        buffer = BytesIO()

        def add_watermark(canvas, doc):
            if pdf_watermark_image_url:
                from plugins.interactors.dms.pdf_blocks.watermark_block import (
                    add_centered_watermark,
                )

                add_centered_watermark(
                    canvas, pdf_watermark_image_url, opacity=0.1, scale=1
                )

        doc = SimpleDocTemplate(
            buffer,
            pagesize=PDFConfig.PAGE_SIZE,
            leftMargin=PDFConfig.MARGIN,
            rightMargin=PDFConfig.MARGIN,
            topMargin=PDFConfig.MARGIN,
            bottomMargin=PDFConfig.MARGIN,
        )

        flowables = self._get_flowables(block_dtos=pdf_block_dtos)
        doc.build(
            flowables, onFirstPage=add_watermark, onLaterPages=add_watermark
        )

        pdf_bytes = buffer.getvalue()
        buffer.close()

        return pdf_bytes

    @staticmethod
    def _add_watermark_to_canvas(
        canvas_obj: canvas, pdf_watermark_image_url: str
    ):
        from plugins.interactors.dms.pdf_blocks.watermark_block import (
            WatermarkCanvas,
        )

        canvas_obj = WatermarkCanvas(
            canvas_obj, image_url=pdf_watermark_image_url, opacity=0.1, scale=1
        )

        return canvas_obj

    def _get_flowables(
        self,
        block_dtos: List[dtos.PDF_BLOCK_UNION_TYPE],
    ) -> List[Flowable]:
        method_map = {
            PDFBlockType.HEADER.value: self._get_header_flowables,
            PDFBlockType.PARAGRAPH.value: self._get_paragraph_flowables,
            PDFBlockType.GRID.value: self._get_grid_block_flowables,
            PDFBlockType.TABLE.value: self._get_table_block_flowables,
            PDFBlockType.LIST.value: self._get_list_block_flowables,
            PDFBlockType.DYNAMIC_TABLE.value: self._add_dynamic_table_block_to_canvas,
        }

        flowables = []
        for block_dto in block_dtos:
            method = method_map.get(block_dto.block_type)
            if not method:
                continue

            flowables += method(block_dto=block_dto)

        return flowables

    @staticmethod
    def _get_header_flowables(
        block_dto: dtos.PDFHeaderBlockDTO,
    ) -> List[Flowable]:
        from plugins.interactors.dms.pdf_flowable_blocks.header_block import (
            HeaderBlockV2,
        )

        header_block = HeaderBlockV2()
        return header_block.create_header_flowables(
            logo_url=block_dto.logo_url,
            header_text=block_dto.header_text,
            sub_header_text=block_dto.sub_header_text,
            sub_sub_header_text=block_dto.sub_sub_header_text,
            right_block_text=block_dto.right_block_text,
        )

    @staticmethod
    def _get_paragraph_flowables(
        block_dto: dtos.PDFParagraphBlockDTO,
    ) -> List[Flowable]:
        from plugins.interactors.dms.pdf_flowable_blocks.paragraph_block import (
            ParagraphBlockV2,
        )

        text_block = ParagraphBlockV2()
        return text_block.create_flowables(
            heading=block_dto.heading,
            lines=block_dto.text_lines,
        )

    @staticmethod
    def _get_grid_block_flowables(
        block_dto: dtos.PDFGridBlockDTO,
    ) -> List[Flowable]:
        from plugins.interactors.dms.pdf_flowable_blocks.grid_block import (
            GridBlockV2,
        )

        grid_units = [
            {
                "text_lines": [
                    text_line for text_line in unit_dto.text_lines if text_line
                ],
                "unit_width": unit_dto.unit_width,
                "alignment": unit_dto.alignment,
            }
            for unit_dto in block_dto.grid_unit_dtos
        ]
        grid_block = GridBlockV2()
        return grid_block.create_grid_flowables(
            heading=block_dto.heading,
            grid_units=grid_units,
        )

    def _get_table_block_flowables(
        self,
        block_dto: dtos.PDFTableBlockDTO,
    ) -> List[Flowable]:
        from plugins.interactors.dms.pdf_flowable_blocks.generic_table_block import (
            CellConfig,
            GenericTableBlockV2,
            RowConfig,
        )

        if not block_dto.table_data:
            return []

        column_widths = self._calculate_table_column_widths(
            column_widths=block_dto.column_widths,
            first_row=block_dto.table_data[0],
        )

        row_config_dtos = []
        for row_values in block_dto.table_data:
            cell_dtos = []
            for index, _value in enumerate(row_values):
                cell_dto = CellConfig(
                    value=_value,
                    width=column_widths[index],
                )
                cell_dtos.append(cell_dto)

            row_config_dto = RowConfig(cells=cell_dtos)
            row_config_dtos.append(row_config_dto)

        table_block = GenericTableBlockV2()
        return table_block.create_generic_table_flowables(
            heading=block_dto.heading, rows=row_config_dtos
        )

    @staticmethod
    def _get_list_block_flowables(
        block_dto: dtos.PDFListBlockDTO,
    ):
        # TODO: Need to support description too
        from plugins.interactors.dms.pdf_flowable_blocks.list_block import (
            ListBlockV2,
        )

        list_block = ListBlockV2()
        return list_block.create_list_flowables(
            heading=block_dto.heading,
            lines=block_dto.text_lines,
            presentation_type=block_dto.presentation_type,
        )

    @staticmethod
    def _add_dynamic_table_block_to_canvas(
        block_dto: dtos.PDFDynamicTableBlockDTO,
    ) -> List[Flowable]:
        from plugins.interactors.dms.pdf_flowable_blocks.generic_table_block import (
            CellConfig,
            GenericTableBlockV2,
            RowConfig,
        )

        row_config_dtos = []
        for row_dto in block_dto.row_dtos:
            row_config_dto = RowConfig(
                cells=[
                    CellConfig(value=cell_dto.text, width=cell_dto.cell_width)
                    for cell_dto in row_dto.cell_dtos
                ]
            )
            row_config_dtos.append(row_config_dto)

        return GenericTableBlockV2().create_generic_table_flowables(
            rows=row_config_dtos,
            heading=block_dto.heading,
        )

    @staticmethod
    def _calculate_table_column_widths(
        column_widths: List[float], first_row: List[Any]
    ):
        total_width = PDFConfig.get_page_width() - (2 * PDFConfig.MARGIN)

        num_columns = len(first_row)

        if column_widths:
            if len(column_widths) != num_columns:
                raise ValueError(
                    "Number of percentages must match number of columns"
                )
            if abs(sum(column_widths) - 100) > 0.01:
                # Allow for floating point imprecision
                raise ValueError("Percentages must sum to 100")
            return [total_width * (pct / 100) for pct in column_widths]

        # Default to equal distribution
        return [total_width / num_columns] * num_columns
