from typing import Optional


def _get_manager_config(config: dict) -> dict:
    from maytak.attachments_handler.attachments_handler import AttachmentsHandler
    from maytak.converters.concrete_converters.binary_converter import BinaryConverter
    from maytak.converters.concrete_converters.docx_converter import DocxConverter
    from maytak.converters.concrete_converters.excel_converter import ExcelConverter
    from maytak.converters.concrete_converters.pdf_converter import PDFConverter
    from maytak.converters.concrete_converters.png_converter import PNGConverter
    from maytak.converters.concrete_converters.pptx_converter import PptxConverter
    from maytak.converters.concrete_converters.txt_converter import TxtConverter
    from maytak.converters.converter_composition import ConverterComposition
    from maytak.metadata_extractors.concrete_metadata_extractors.base_metadata_extractor import BaseMetadataExtractor
    from maytak.metadata_extractors.concrete_metadata_extractors.docx_metadata_extractor import DocxMetadataExtractor
    from maytak.metadata_extractors.concrete_metadata_extractors.image_metadata_extractor import ImageMetadataExtractor
    from maytak.metadata_extractors.concrete_metadata_extractors.note_metadata_extarctor import NoteMetadataExtractor
    from maytak.metadata_extractors.concrete_metadata_extractors.pdf_metadata_extractor import PdfMetadataExtractor
    from maytak.metadata_extractors.metadata_extractor_composition import MetadataExtractorComposition
    from maytak.readers.archive_reader.archive_reader import ArchiveReader
    from maytak.readers.article_reader.article_reader import ArticleReader
    from maytak.readers.csv_reader.csv_reader import CSVReader
    from maytak.readers.docx_reader.docx_reader import DocxReader
    from maytak.readers.email_reader.email_reader import EmailReader
    from maytak.readers.excel_reader.excel_reader import ExcelReader
    from maytak.readers.html_reader.html_reader import HtmlReader
    from maytak.readers.json_reader.json_reader import JsonReader
    from maytak.readers.mhtml_reader.mhtml_reader import MhtmlReader
    from maytak.readers.note_reader.note_reader import NoteReader
    from maytak.readers.pdf_reader.pdf_auto_reader.pdf_auto_reader import PdfAutoReader
    from maytak.readers.pdf_reader.pdf_image_reader.pdf_image_reader import PdfImageReader
    from maytak.readers.pdf_reader.pdf_txtlayer_reader.pdf_tabby_reader import PdfTabbyReader
    from maytak.readers.pdf_reader.pdf_txtlayer_reader.pdf_txtlayer_reader import PdfTxtlayerReader
    from maytak.readers.pptx_reader.pptx_reader import PptxReader
    from maytak.readers.reader_composition import ReaderComposition
    from maytak.readers.txt_reader.raw_text_reader import RawTextReader
    from maytak.structure_constructors.concrete_structure_constructors.linear_constructor import LinearConstructor
    from maytak.structure_constructors.concrete_structure_constructors.tree_constructor import TreeConstructor
    from maytak.structure_constructors.structure_constructor_composition import StructureConstructorComposition
    from maytak.structure_extractors.concrete_structure_extractors.article_structure_extractor import ArticleStructureExtractor
    from maytak.structure_extractors.concrete_structure_extractors.classifying_law_structure_extractor import ClassifyingLawStructureExtractor
    from maytak.structure_extractors.concrete_structure_extractors.default_structure_extractor import DefaultStructureExtractor
    from maytak.structure_extractors.concrete_structure_extractors.diploma_structure_extractor import DiplomaStructureExtractor
    from maytak.structure_extractors.concrete_structure_extractors.fintoc_structure_extractor import FintocStructureExtractor
    from maytak.structure_extractors.concrete_structure_extractors.foiv_law_structure_extractor import FoivLawStructureExtractor
    from maytak.structure_extractors.concrete_structure_extractors.law_structure_excractor import LawStructureExtractor
    from maytak.structure_extractors.concrete_structure_extractors.tz_structure_extractor import TzStructureExtractor
    from maytak.structure_extractors.structure_extractor_composition import StructureExtractorComposition

    converters = [
        DocxConverter(config=config),
        ExcelConverter(config=config),
        PptxConverter(config=config),
        TxtConverter(config=config),
        PDFConverter(config=config),
        PNGConverter(config=config),
        BinaryConverter(config=config)
    ]
    readers = [
        ArticleReader(config=config),
        DocxReader(config=config),
        ExcelReader(config=config),
        PptxReader(config=config),
        RawTextReader(config=config),
        CSVReader(config=config),
        HtmlReader(config=config),
        NoteReader(config=config),
        JsonReader(config=config),
        ArchiveReader(config=config),
        PdfAutoReader(config=config),
        PdfTabbyReader(config=config),
        PdfTxtlayerReader(config=config),
        PdfImageReader(config=config),
        EmailReader(config=config),
        MhtmlReader(config=config)
    ]

    metadata_extractors = [
        DocxMetadataExtractor(config=config),
        PdfMetadataExtractor(config=config),
        ImageMetadataExtractor(config=config),
        NoteMetadataExtractor(config=config),
        BaseMetadataExtractor(config=config)
    ]

    law_extractors = {
        FoivLawStructureExtractor.document_type: FoivLawStructureExtractor(config=config),
        LawStructureExtractor.document_type: LawStructureExtractor(config=config)
    }
    structure_extractors = {
        DefaultStructureExtractor.document_type: DefaultStructureExtractor(config=config),
        DiplomaStructureExtractor.document_type: DiplomaStructureExtractor(config=config),
        TzStructureExtractor.document_type: TzStructureExtractor(config=config),
        ClassifyingLawStructureExtractor.document_type: ClassifyingLawStructureExtractor(extractors=law_extractors, config=config),
        ArticleStructureExtractor.document_type: ArticleStructureExtractor(config=config),
        FintocStructureExtractor.document_type: FintocStructureExtractor(config=config)
    }

    return dict(
        converter=ConverterComposition(converters=converters),
        reader=ReaderComposition(readers=readers),
        structure_extractor=StructureExtractorComposition(extractors=structure_extractors, default_key="other", config=config),
        structure_constructor=StructureConstructorComposition(
            constructors={"linear": LinearConstructor(), "tree": TreeConstructor()},
            default_constructor=TreeConstructor()
        ),
        document_metadata_extractor=MetadataExtractorComposition(extractors=metadata_extractors),
        attachments_handler=AttachmentsHandler(config=config)
    )


class ConfigurationManager(object):
    """
    Pattern Singleton for configuration service
    INFO: Configuration class and config are created once at the first call
    For initialization ConfigurationManager call ConfigurationManager.getInstance().initConfig(new_config: dict)
    If you need default config, call ConfigurationManager.getInstance()
    """
    __instance = None
    __config = None

    @classmethod
    def get_instance(cls: "ConfigurationManager") -> "ConfigurationManager":
        """
        Actual object creation will happen when we use ConfigurationManager.getInstance()
        """
        if not cls.__instance:
            cls.__instance = ConfigurationManager()

        return cls.__instance

    def init_config(self, config: dict, new_config: Optional[dict] = None) -> None:
        if new_config is None:
            self.__config = _get_manager_config(config)
        else:
            self.__config = new_config

    def get_config(self, config: dict) -> dict:
        if self.__config is None:
            self.init_config(config)
        return self.__config


def get_manager_config(config: dict) -> dict:
    return ConfigurationManager().get_instance().get_config(config)
