"""
Ponto de partida do módulo de blocos. Usado para limpar e organizar
os blocos em arquivos individuais baseados na proposta.
Mas fornece todos via o módulo "blocks"
"""

from django.utils.translation import gettext_lazy as _
from wagtail import blocks





from .layout_blocks import HeroBlock 
from .layout_blocks import GridBlock 
from .layout_blocks import CardGridBlock
from .layout_blocks import EnapCardGridBlock
from .layout_blocks import EnapBannerBlock
from .layout_blocks import EnapFooterGridBlock
from .layout_blocks import EnapFooterSocialGridBlock
from .layout_blocks import EnapSectionBlock
from enap_designsystem.blocks.base_blocks import ButtonGroupBlock
from enap_designsystem.blocks.base_blocks import CarouselBlock


from .content_blocks import CardBlock
from .content_blocks import EnapCardBlock
from .content_blocks import EnapAccordionBlock

from .content_blocks import FeatureImageTextBlock
from .content_blocks import EnapFooterLinkBlock
from .content_blocks import EnapAccordionPanelBlock
from .content_blocks import EnapAccordionBlock
from .content_blocks import EnapNavbarLinkBlock
from .html_blocks import CourseIntroTopicsBlock
from .html_blocks import WhyChooseEnaptBlock
from .html_blocks import CourseFeatureBlock
from .html_blocks import CourseModulesBlock
from .html_blocks import ProcessoSeletivoBlock
from .html_blocks import TeamCarouselBlock
from .html_blocks import TestimonialsCarouselBlock
from .html_blocks import PreviewCoursesBlock

from .html_blocks import ButtonBlock
from .html_blocks import DownloadBlock
from .html_blocks import ImageBlock
from .html_blocks import ImageLinkBlock
from .html_blocks import QuoteBlock
from .html_blocks import RichTextBlock
from .html_blocks import PageListBlock
from .html_blocks import NewsCarouselBlock
from .html_blocks import CoursesCarouselBlock
from .html_blocks import SuapCourseBlock
from .html_blocks import EventsCarouselBlock
from .html_blocks import DropdownBlock

HTML_STREAMBLOCKS = [
    ("text", RichTextBlock(icon="cr-font")),
    ("button", ButtonBlock()),
    ("image", ImageBlock()),
    ("image_link", ImageLinkBlock()),
    (
        "html",
        blocks.RawHTMLBlock(
            icon="code",
            form_classname="monospace",
            label=_("HTML"),
        ),
    ),
    ("download", DownloadBlock()),
    ("quote", QuoteBlock()),
]


CONTENT_STREAMBLOCKS = HTML_STREAMBLOCKS + [
    ("accordion", EnapAccordionBlock()),
    ("card", CardBlock()),
    ("card2", EnapCardBlock()),

]

"""
Exemplo de estrutura no codered
    (
        "hero",
        HeroBlock(
            [
                ("row", GridBlock(CONTENT_STREAMBLOCKS)),
                (
                    "cardgrid",
                    CardGridBlock(
                        [
                            ("card", CardBlock()),
                        ]
                    ),
                ),
                (
                    "html",
                    blocks.RawHTMLBlock(
                        icon="code", form_classname="monospace", label=_("HTML")
                    ),
                ),
            ]
        ),
    ),
"""

LAYOUT_STREAMBLOCKS = [
    (
        "enap_herobanner", EnapBannerBlock()
    ),
    ("accordion", EnapAccordionBlock()),

    (
        "enap_herofeature", FeatureImageTextBlock()
    ),
    ("enap_herofeature", FeatureImageTextBlock()),

    ("banner", EnapBannerBlock()),

    ('feature_course', CourseFeatureBlock()),

    ('feature_processo_seletivo', ProcessoSeletivoBlock()),

    ('team_carousel', TeamCarouselBlock()),

    ('testimonials_carousel', TestimonialsCarouselBlock()),

    ('why_choose', WhyChooseEnaptBlock()),

    ("enap_accordion", EnapAccordionBlock()),

    ('button_group', ButtonGroupBlock()),

    ('carousel', CarouselBlock()),

    ('dropdown', DropdownBlock()),

    ("courses_carousel", CoursesCarouselBlock()),

    ('course_intro_topics', CourseIntroTopicsBlock()),

    ('why_choose', WhyChooseEnaptBlock()),

    ('testimonials_carousel', TestimonialsCarouselBlock()),

    ("preview_courses", PreviewCoursesBlock()),

    ('feature_processo_seletivo', ProcessoSeletivoBlock()),

    ('team_carousel', TeamCarouselBlock()),

    ('feature_estrutura', CourseModulesBlock()),    

    ('carousel', CarouselBlock()),
    ("download", DownloadBlock()),
    ("noticias_carousel", NewsCarouselBlock()),
    ("eventos_carousel", EventsCarouselBlock()),

    (
        "enap_section", EnapSectionBlock([
    ("enap_cardgrid", EnapCardGridBlock([
        ("enap_card", EnapCardBlock()),
    ])),
    ("enap_accordion", EnapAccordionBlock()),  # Adicionada a vírgula aqui
    ("richtext", RichTextBlock()),  # Corrigida a formatação aqui
    ("button", ButtonBlock()),
    ("image", ImageBlock()),
    ("quote", QuoteBlock()),
    ("preview_courses", PreviewCoursesBlock()),
    ("noticias_carousel", NewsCarouselBlock()),
    ("enap_herofeature", FeatureImageTextBlock()),
    ('feature_course', CourseFeatureBlock()),
    ('feature_estrutura', CourseModulesBlock()),
])
    )
]




DYNAMIC_CARD_STREAMBLOCKS = [
    (
        "enap_section", EnapSectionBlock([
            ("enap_cardgrid", EnapCardGridBlock([
                ("enap_card", EnapCardBlock()),
            ])),
        ])
    ),

    ("page_list", PageListBlock()),
]


CARD_CARDS_STREAMBLOCKS = [
    (
        "enap_section", EnapSectionBlock([
            ("enap_cardgrid", EnapCardGridBlock([
                ("enap_card", EnapCardBlock()),
            ]))
        ])
    )
]

