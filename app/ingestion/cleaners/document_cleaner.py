from ..models.document import ParsedDocument, DocumentSection
from .text_cleaner import TextCleaner


class DocumentCleaner:

    @staticmethod
    def clean(document: ParsedDocument) -> ParsedDocument:
        cleaned_sections = []

        for section in document.sections:
            cleaned_sections.append(
                DocumentSection(
                    section_id=section.section_id,
                    title=TextCleaner.clean(section.title),
                    content=TextCleaner.clean(section.content),
                    page_number=section.page_number,
                )
            )

        cleaned_full_text = TextCleaner.clean(
            document.full_text
        )

        return ParsedDocument(
            document_name=document.document_name,
            document_type=document.document_type,
            source_path=document.source_path,
            full_text=cleaned_full_text,
            sections=cleaned_sections,
        )
