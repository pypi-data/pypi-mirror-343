
from django.utils.translation import gettext_lazy as _
from wagtail import blocks
from types import SimpleNamespace


from enap_designsystem.blocks.base_blocks import CarouselBlock
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.search import index
from wagtail import blocks
from datetime import datetime
import warnings
from wagtail.images.blocks import ImageChooserBlock

from wagtail.contrib.table_block.blocks import TableBlock as WagtailTableBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.admin.panels import FieldPanel
from wagtail.blocks import StructBlock, CharBlock, RichTextBlock
from wagtail.images.blocks import ImageChooserBlock

from .base_blocks import BaseBlock
from .base_blocks import BaseLinkBlock
from .base_blocks import ButtonMixin
from .base_blocks import CoderedAdvTrackingSettings
from .base_blocks import LinkStructValue
from .base_blocks import BaseBlock, ButtonMixin, BaseLinkBlock, LinkStructValue, CoderedAdvTrackingSettings

class ButtonBlock(ButtonMixin, BaseLinkBlock):
    """
    A link styled as a button.
    """
    
    type_class = blocks.ChoiceBlock(
		choices=[
			('primary', 'Tipo primário'),
			('secondary', 'Tipo secundário'),
			('terciary', 'Tipo terciário'),
		],
		default='primary',
		help_text="Escolha o tipo do botão",
		label="Tipo de botão"
	)

    size_class = blocks.ChoiceBlock(
		choices=[
			('small', 'Pequeno'),
			('medium', 'Médio'),
			('large', 'Grande'),
			('extra-large', 'Extra grande'),
		],
		default='small',
		help_text="Escolha o tamanho do botão",
		label="Tamanho"
	)

    icone_bool = blocks.BooleanBlock(
        required=False,
        label=_("Icone"),
    )

    # Tentando remover campos herdados do codered
    button_style = None
    button_size = None
    page = None
    document = None
    downloadable_file = None
    class Meta:
        template = "enap_designsystem/blocks/button_block.html"
        icon = "cr-hand-pointer-o"
        label = _("Button Link")
        value_class = LinkStructValue

class DownloadBlock(ButtonMixin, BaseBlock):
    """
    Link to a file that can be downloaded.
    """

    downloadable_file = DocumentChooserBlock(
        required=False,
        label=_("Document link"),
    )

    class Meta:
        template = "enap_designsystem/blocks/download_block.html"
        icon = "download"
        label = _("Download")
    
class ImageBlock(BaseBlock):
    """
    An <img>, by default styled responsively to fill its container.
    """

    image = ImageChooserBlock(
        label=_("Image"),
    )

    class Meta:
        template = "coderedcms/blocks/image_block.html"
        icon = "image"
        label = _("Image")

class ImageLinkBlock(BaseLinkBlock):
    """
    An <a> with an image inside it, instead of text.
    """

    image = ImageChooserBlock(
        label=_("Image"),
    )
    alt_text = blocks.CharBlock(
        max_length=255,
        required=True,
        help_text=_("Alternate text to show if the image doesn’t load"),
    )

    class Meta:
        template = "coderedcms/blocks/image_link_block.html"
        icon = "image"
        label = _("Image Link")
        value_class = LinkStructValue

class QuoteBlock(BaseBlock):
    """
    A <blockquote>.
    """

    text = blocks.TextBlock(
        required=True,
        rows=4,
        label=_("Quote Text"),
    )
    author = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_("Author"),
    )

    class Meta:
        template = "coderedcms/blocks/quote_block.html"
        icon = "openquote"
        label = _("Quote")


class RichTextBlock(blocks.RichTextBlock):
    class Meta:
        template = "coderedcms/blocks/rich_text_block.html"

class PagePreviewBlock(BaseBlock):
    """
    Renders a preview of a specific page.
    """

    page = blocks.PageChooserBlock(
        required=True,
        label=_("Page to preview"),
        help_text=_("Show a mini preview of the selected page."),
    )

    class Meta:
        template = "enap_designsystem/blocks/pagepreview_block.html"
        icon = "doc-empty-inverse"
        label = _("Page Preview")



class PreviewCoursesBlock(BaseBlock):
    """
    Renders a preview of a specific page.
    """

    page = blocks.PageChooserBlock(
        required=True,
        label=_("Pagina de Formações"),
        help_text=_("Show a mini preview of the selected page."),
    )

    class Meta:
        template = "enap_designsystem/blocks/preview_courses.html"
        icon = "doc-empty-inverse"
        label = _("Pagina de Formações")





class PageListBlock(BaseBlock):
    """
    Renders a preview of selected pages.
    """

    indexed_by = blocks.PageChooserBlock(
        required=True,
        label=_("Parent page"),
        help_text=_(
            "Show a preview of pages that are children of the selected page. "
            "Uses ordering specified in the page’s LAYOUT tab."
        ),
    )
    
    # DEPRECATED: Remove in 3.0
    show_preview = blocks.BooleanBlock(
        required=False,
        default=False,
        label=_("Show body preview"),
    )
    num_posts = blocks.IntegerBlock(
        default=3,
        label=_("Number of pages to show"),
    )

    class Meta:
        template = "enap_designsystem/blocks/page/pagelist_block.html"
        icon = "list-ul"
        label = _("Latest Pages")

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)

        indexer = value["indexed_by"].specific
        # try to use the CoderedPage `get_index_children()`,
        # but fall back to get_children if this is a non-CoderedPage
        if hasattr(indexer, "get_index_children"):
            pages = indexer.get_index_children()
            
        else:
            pages = indexer.get_children().live()

        context["pages"] = pages[: value["num_posts"]]
        return context




class NewsCarouselBlock(BaseBlock):
    """
    Renders a carousel of selected news pages.
    """

    indexed_by = blocks.PageChooserBlock(
        required=True,
        label=_("Parent page"),
        help_text=_(
            "Show a preview of pages that are children of the selected page. "
            "Uses ordering specified in the page’s LAYOUT tab."
        ),
    )
    
    num_posts = blocks.IntegerBlock(
        default=3,
        label=_("Number of pages to show"),
    )

    class Meta:
        template = "enap_designsystem/blocks/page/pagenoticias_block.html"
        icon = "list-ul"
        label = _("News Carousel")

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)

        indexer = value["indexed_by"].specific
        
        if hasattr(indexer, "get_index_children"):
            pages = indexer.get_index_children()
        else:
            pages = indexer.get_children().live()

        context["pages"] = pages[: value["num_posts"]]
        return context
    

class CoursesCarouselBlock(BaseBlock):
    """
    Renders a carousel of selected news pages.
    """

    indexed_by = blocks.PageChooserBlock(
        required=True,
        label=_("Parent page"),
        help_text=_(
            "Show a preview of pages that are children of the selected page. "
            "Uses ordering specified in the page’s LAYOUT tab."
        ),
    )
    
    num_posts = blocks.IntegerBlock(
        default=3,
        label=_("Number of pages to show"),
    )

    class Meta:
        template = "enap_designsystem/blocks/card_courses.html"
        icon = "list-ul"
        label = _("News Courses")

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)

        indexer = value["indexed_by"].specific
        
        if hasattr(indexer, "get_index_children"):
            pages = indexer.get_index_children()
        else:
            pages = indexer.get_children().live()

        context["pages"] = pages[: value["num_posts"]]
        return context


class SuapCourseBlock(StructBlock):
    title = CharBlock(required=False, label="Título")
    description = CharBlock(required=False, label="Descrição")
    num_items = blocks.IntegerBlock(default=3,label=_("Máximo de cursos apresentados"),)

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)
        num = value.get("num_items", 3)
        cursos_suap = self.get_destaques(num)
        context.update({
            "bloco_suap": value,
            "cursos_suap": cursos_suap
        })

        return context

    def get_destaques(self, limit=None):
        import requests
        try:
            resp = requests.get("https://bff-portal.enap.gov.br/v1/home/destaques", timeout=5)
            resp.raise_for_status()
            data = resp.json()
            if limit:
                data = data[: limit]
            return [SimpleNamespace(**item) for item in data]
        except Exception as e:
            return []

    class Meta:
        template = "enap_designsystem/blocks/suap/suap_courses_block.html"
        icon = "list-ul"
        label = "Cursos do SUAP"



class DropdownBlock(blocks.StructBlock):
    label = blocks.CharBlock(required=True)
    options = blocks.ListBlock(blocks.StructBlock([
        ('title', blocks.CharBlock(required=True)),
        ('page', blocks.PageChooserBlock(required=True))
    ]))

    class Meta:
        template = 'enap_designsystem/pages/mini/dropdown-holofote_blocks.html'
        icon = 'arrow_drop_down'
        label = 'Dropdown'




class EventsCarouselBlock(BaseBlock):
    """
    Renders a carousel of selected event pages.
    """

    indexed_by = blocks.PageChooserBlock(
        required=True,
        label=_("Parent page"),
        help_text=_(
            "Show a preview of pages that are children of the selected page. "
            "Uses ordering specified in the page's LAYOUT tab."
        ),
    )

    num_posts = blocks.IntegerBlock(
        default=3,
        label=_("Number of pages to show"),
    )

    class Meta:
        template = "enap_designsystem/pages/mini/eventos.html"
        icon = "date"
        label = _("Events Carousel")

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)

        indexer = value["indexed_by"].specific
        
        if hasattr(indexer, "get_index_children"):
            pages = indexer.get_index_children()
        else:
            pages = indexer.get_children().live()

        context["pages"] = pages[: value["num_posts"]]
        return context
    

class CourseFeatureBlock(blocks.StructBlock):
    title_1 = blocks.CharBlock(required=True, help_text="Primeiro título da feature", default="Título da feature")
    description_1 = blocks.TextBlock(required=True, help_text="Primeira descrição da feature", default="Descrição da feature")
    title_2 = blocks.CharBlock(required=True, help_text="Segundo título da feature", default="Título da feature")
    description_2 = blocks.TextBlock(required=True, help_text="Segunda descrição da feature", default="Descrição da feature")
    image = ImageChooserBlock(required=False, help_text="Imagem da feature do curso")
    
    class Meta:
        template = "enap_designsystem/blocks/feature_course.html"
        icon = "placeholder"
        label = "Feature de Curso"
        initialized = True



class CourseModulesBlock(blocks.StructBlock):
    """Bloco de estrutura do curso com múltiplos dropdowns."""
    title = blocks.CharBlock(required=True, default="Estrutura do curso", help_text="Título da seção")
    
    modules = blocks.ListBlock(
        blocks.StructBlock([
            # Ordem invertida - module_title é o primeiro campo agora
            ("module_title", blocks.CharBlock(required=True, help_text="Título do módulo (ex: 1º Módulo)", default="1º Módulo")),
            ("module_description", blocks.TextBlock(required=True, help_text="Descrição breve do módulo", default="Descreva o módulo")),
            ("module_items", blocks.ListBlock(
                blocks.CharBlock(required=True, help_text="Item da lista de conteúdo do módulo")
            )),
        ]),
        min_num=1,
        help_text="Adicione os módulos do curso"
    )
    
    class Meta:
        template = "enap_designsystem/blocks/feature_estrutura.html"
        icon = "list-ol"
        label = "Estrutura do Curso"
        initialized = True




class CourseIntroTopicsBlock(StructBlock):
    """Componente com introdução e tópicos fixos do curso."""
    title = CharBlock(label="Título do Curso", required=True, help_text="Título principal sobre o curso", default="Título do Curso")
    description = RichTextBlock(label="Descrição do Curso", required=True, help_text="Descrição geral do curso", default="Descreva o curso")
    image = ImageChooserBlock(label="Imagem", required=True, help_text="Imagem para destacar o curso")
    
    # Tópicos fixos com apenas descrições editáveis
    modalidade_description = RichTextBlock(label="Descrição da Modalidade", required=True, help_text="Descreva a modalidade do curso", default="Descreva a modalidade do curso")
    curso_description = RichTextBlock(label="Descrição do Curso", required=True, help_text="Descreva o conteúdo do curso", default="Descreva o conteúdo do curso")
    metodologia_description = RichTextBlock(label="Descrição da Metodologia", required=True, help_text="Descreva a metodologia do curso", default="Descreva a metodologia do curso")
    
    class Meta:
        template = 'enap_designsystem/blocks/course_intro_topics.html'
        icon = 'doc-full'
        label = 'Introdução e Tópicos do Curso'




class WhyChooseEnaptBlock(blocks.StructBlock):
    """Seção 'Por que escolher a Enap?'"""
    # Título e descrição principal
    title = blocks.CharBlock(required=True, label=_("Título principal"), default="Titulo do beneficio")
    description = blocks.TextBlock(required=False, label=_("Descrição principal"), default="Titulo do beneficio")
    
    # Benefício 1
    image_1 = ImageChooserBlock(required=False, label=_("Imagem do benefício 1"))
    title_1 = blocks.CharBlock(required=True, label=_("Título do benefício 1"), default="Metodologia ensino–aplicação")
    
    # Benefício 2
    image_2 = ImageChooserBlock(required=False, label=_("Imagem do benefício 2"))
    title_2 = blocks.CharBlock(required=True, label=_("Título do benefício 2"), default="Desenvolvimento de competências de forma inovadora")
    
    # Benefício 3
    image_3 = ImageChooserBlock(required=False, label=_("Imagem do benefício 3"))
    title_3 = blocks.CharBlock(required=True, label=_("Título do benefício 3"), default="Desenvolvimento de competências de forma inovadora")
    
    # Benefício 4
    image_4 = ImageChooserBlock(required=False, label=_("Imagem do benefício 4"))
    title_4 = blocks.CharBlock(required=True, label=_("Título do benefício 4"), default="Desenvolvimento de competências de forma inovadora")

    class Meta:
        template = 'enap_designsystem/blocks/why_choose.html'
        icon = 'placeholder'
        label = _("Titulo do beneficio")





class ProcessoSeletivoBlock(blocks.StructBlock):
    """Bloco para exibir informações sobre o processo seletivo com 3 módulos."""
    title = blocks.CharBlock(required=True, default="Processo seletivo", help_text="Título da seção")
    description = blocks.TextBlock(required=True, default="Sobre o processo seletivo", help_text="Descrição do processo seletivo")
    
    # Módulo 1
    module1_title = blocks.CharBlock(required=True, default="Inscrição", help_text="Título do primeiro módulo")
    module1_description = blocks.TextBlock(required=True, help_text="Descrição do primeiro módulo", default="Lorem ipsum dolor sit amet, lorem ipsum dolor sit amet")
    
    # Módulo 2
    module2_title = blocks.CharBlock(required=True, default="Seleção", help_text="Título do segundo módulo")
    module2_description = blocks.TextBlock(required=True, help_text="Descrição do segundo módulo", default="Lorem ipsum dolor sit amet, lorem ipsum dolor sit amet")
    
    # Módulo 3
    module3_title = blocks.CharBlock(required=True, default="Resultado", help_text="Título do terceiro módulo")
    module3_description = blocks.TextBlock(required=True, help_text="Descrição do terceiro módulo", default="Lorem ipsum dolor sit amet, lorem ipsum dolor sit amet")
    
    class Meta:
        template = "enap_designsystem/blocks/feature_processo_seletivo.html"
        icon = "list-ul"
        label = "Processo Seletivo"
        initialized = True




class TeamCarouselBlock(blocks.StructBlock):
    """Carrossel para exibir membros da equipe."""
    title = blocks.CharBlock(required=True, default="Nossa Equipe", help_text="Título da seção")
    description = blocks.TextBlock(required=True, help_text="Descrição da seção da equipe", default="Equipe de desenvolvedores e etc")
    view_all_text = blocks.CharBlock(required=False, default="Ver todos", help_text="Texto do botão 'ver todos'")
    
    members = blocks.ListBlock(
        blocks.StructBlock([
            ("name", blocks.CharBlock(required=True, help_text="Nome do membro da equipe")),
            ("role", blocks.CharBlock(required=True, help_text="Cargo/função do membro")),
            ("image", ImageChooserBlock(required=False, help_text="Foto do membro da equipe")),
        ]),
        help_text="Adicione os membros da equipe",
        default=[
            {'name': 'Membro 1', 'role': 'Cargo 1', 'image': None},
            {'name': 'Membro 2', 'role': 'Cargo 2', 'image': None},
            {'name': 'Membro 3', 'role': 'Cargo 3', 'image': None},
            {'name': 'Membro 4', 'role': 'Cargo 4', 'image': None},
        ],
        collapsed=False
    )

    class Meta:
        template = 'enap_designsystem/blocks/team_carousel.html'
        icon = 'group'
        label = 'Carrossel de Equipe'




class TestimonialsCarouselBlock(blocks.StructBlock):
    """Carrossel para exibir depoimentos ou testemunhos."""
    title = blocks.CharBlock(required=True, default="Depoimentos", help_text="Título da seção")
    description = blocks.TextBlock(required=False, help_text="Descrição opcional da seção")
    
    testimonials = blocks.ListBlock(
        blocks.StructBlock([
            ("name", blocks.CharBlock(required=True, help_text="Nome da pessoa", default="Nome do profissional")),
            ("position", blocks.CharBlock(required=True, help_text="Cargo ou posição da pessoa", default="Cargo do profissional")),
            ("testimonial", blocks.TextBlock(required=True, help_text="Depoimento da pessoa", default="Lorem ipsum dolor sit amet, lorem ipsum dolor sit amet")),
            ("image", ImageChooserBlock(required=True, help_text="Foto da pessoa")),
        ]),
        help_text="Adicione os depoimentos"
    )
    
    class Meta:
        template = 'enap_designsystem/blocks/testimonials_carousel.html'
        icon = 'openquote'
        label = 'Carrossel de Depoimentos'







# Definição dos blocos de conteúdo para o StreamField
class HeadingBlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=True)
    level = blocks.ChoiceBlock(choices=[
        ('h2', 'Título Nível 2'),
        ('h3', 'Título Nível 3'),
        ('h4', 'Título Nível 4'),
    ], default='h2')

    class Meta:
        template = 'blocks/heading_block.html'
        icon = 'title'
        label = 'Título'


class RichTextBlock(blocks.RichTextBlock):
    class Meta:
        template = 'enap_designsystem/blocks/richtext_block.html'
        icon = 'doc-full'
        label = 'Texto'


class ImageBlock(blocks.StructBlock):
    image = ImageChooserBlock(required=True) 
    caption = blocks.CharBlock(required=False)
    
    class Meta:
        template = 'enap_designsystem/blocks/image_block.html'
        icon = 'image'
        label = 'Imagem'

class QuoteBlock(blocks.StructBlock):
    quote = blocks.TextBlock(required=True)
    attribution = blocks.CharBlock(required=False)
    
    class Meta:
        template = 'enap_designsystem/blocks/quote_block.html'
        icon = 'openquote'
        label = 'Citação'


class VideoBlock(blocks.StructBlock):
    url = blocks.URLBlock(required=True, help_text="URL do YouTube ou Vimeo")
    caption = blocks.CharBlock(required=False)
    
    class Meta:
        template = 'enap_designsystem/blocks/video_block.html'
        icon = 'media'
        label = 'Embed Vídeo'

ARTICLE_STREAMBLOCKS = [
    ('richtext', RichTextBlock()),
    ("button", ButtonBlock()),
    ('image', ImageBlock()),
    ('quote', QuoteBlock()),
    ('carousel', CarouselBlock()),
    ("download", DownloadBlock()),
    ("embed_video", VideoBlock()),
    ("noticias_carousel", NewsCarouselBlock()),
    ("eventos_carousel", EventsCarouselBlock()),
]

class ArticlePage(Page):
    """
    Página de artigo, adequada para notícias ou conteúdo de blog.
    """

    class Meta:
        verbose_name = _("ENAP Artigo")
        verbose_name_plural = _("ENAP Artigos")

    template = "enap_designsystem/blocks/article_page.html"

    # Campo para o conteúdo principal
    body = StreamField(
        ARTICLE_STREAMBLOCKS,
        null=True,
        blank=True,
        verbose_name=_("Conteúdo"),
        use_json_field=True,
    )

    # Campos de metadados do artigo
    caption = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Legenda"),
    )
    
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        editable=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Autor"),
        related_name='enap_articlepage_set',
    )
    
    author_display = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Exibir autor como"),
        help_text=_("Substitui como o nome do autor é exibido neste artigo."),
    )
    
    date_display = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Data de publicação para exibição"),
    )

    # Campos para SEO e compartilhamento
    featured_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_("Imagem destacada"),
        help_text=_("Imagem usada para compartilhamento em redes sociais e listagens"),
    )

    # Propriedades para SEO e exibição de metadados
    @property
    def seo_author(self) -> str:
        """
        Obtém o nome do autor usando uma estratégia de fallback.
        """
        if self.author_display:
            return self.author_display
        if self.author:
            return self.author.get_full_name()
        if self.owner:
            return self.owner.get_full_name()
        return ""

    @property
    def seo_published_at(self) -> datetime:
        """
        Obtém a data de publicação para exibição.
        """
        if self.date_display:
            return self.date_display
        return self.first_published_at

    @property
    def seo_description(self) -> str:
        """
        Obtém a descrição usando uma estratégia de fallback.
        """
        if self.search_description:
            return self.search_description
        if self.caption:
            return self.caption
        return self.get_body_preview(100)

    @property
    def get_body_preview(self, length=100) -> str:
        """
        Obtém uma prévia do conteúdo do artigo.
        """
        text = ""
        for block in self.body:
            if block.block_type == 'richtext':
                text += block.value.source
            elif block.block_type == 'heading':
                text += block.value['heading'] + " "
        
        # Remover tags HTML e limitar caracteres
        import re
        text = re.sub(r'<[^>]+>', '', text)
        return text[:length] + "..." if len(text) > length else text

    @property
    def url_filter(self):
        if hasattr(self, 'full_url') and self.full_url:
            return self.full_url
        return self.get_url_parts()[2] if self.get_url_parts() else ""
    
        
    # Configuração de busca
    search_fields = Page.search_fields + [
        index.SearchField('body'),
        index.SearchField('caption', boost=2),
        index.FilterField('author'),
        index.FilterField('author_display'),
        index.FilterField('date_display'),
        index.FilterField("url", name="url_filter"),
    ]

    # Painéis de conteúdo para o admin
    content_panels = Page.content_panels + [
        FieldPanel('body'),
        FieldPanel('caption'),
        FieldPanel('featured_image'),
        MultiFieldPanel(
            [
                FieldPanel('author'),
                FieldPanel('author_display'),
                FieldPanel('date_display'),
            ],
            heading=_("Informações de Publicação"),
        ),
    ]
    
    def get_searchable_content(self):
        content = super().get_searchable_content()
        content.append(self.caption or "")
        content.append(self.seo_description or "")
        content.append(self.get_body_preview())
        return content
    
    # Métodos auxiliares para templates
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        # Você pode adicionar variáveis de contexto específicas para artigos aqui
        return context


class ArticleIndexPage(Page):
    """
    Página de índice que mostra uma lista de artigos.
    """

    class Meta:
        verbose_name = _("ENAP Página de Índice de Artigos")
        verbose_name_plural = _("ENAP Páginas de Índice de Artigos")

    template = "enap_designsystem/pages/article_index_page.html"

    # Introdução para a página de listagem
    intro = models.TextField(
        blank=True,
        verbose_name=_("Introdução"),
    )
    
    # Opções de exibição dos artigos
    show_images = models.BooleanField(
        default=True,
        verbose_name=_("Exibir imagens"),
    )
    
    show_captions = models.BooleanField(
        default=True,
        verbose_name=_("Exibir legendas"),
    )
    
    show_meta = models.BooleanField(
        default=True,
        verbose_name=_("Exibir autor e informações de data"),
    )
    
    show_preview_text = models.BooleanField(
        default=True,
        verbose_name=_("Exibir texto de prévia"),
    )
    
    articles_per_page = models.PositiveIntegerField(
        default=10,
        verbose_name=_("Artigos por página"),
    )

    # Configuração de busca
    search_fields = Page.search_fields + [
        index.SearchField('intro'),
    ]

    # Painéis de conteúdo para o admin
    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        MultiFieldPanel(
            [
                FieldPanel('show_images'),
                FieldPanel('show_captions'),
                FieldPanel('show_meta'),
                FieldPanel('show_preview_text'),
                FieldPanel('articles_per_page'),
            ],
            heading=_("Exibição de artigos"),
        ),
    ]

    def get_searchable_content(self):
        content = super().get_searchable_content()
        content.append(self.intro or "")
        content.append(self.search_description or "")
        return content
    
    def get_context(self, request, *args, **kwargs):
        """
        Adiciona artigos ao contexto.
        """
        context = super().get_context(request, *args, **kwargs)
        
        # Obtém todos os artigos
        articles = ArticlePage.objects.live().descendant_of(self)
        
        # Ordena por data (mais recente primeiro)
        articles = articles.order_by('-date_display', '-first_published_at')
        
        # Paginação
        from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
        paginator = Paginator(articles, self.articles_per_page)
        page = request.GET.get('page')
        
        try:
            articles = paginator.page(page)
        except PageNotAnInteger:
            articles = paginator.page(1)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)
        
        context['articles'] = articles
        return context