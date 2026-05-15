#!/usr/bin/env python3
"""
WorldAnvil JSON export → Markdown converter.

Usage:
    python tools/wa-to-md.py export/World-Tyrnarra-ec6 worldanvil-export/Tyrnarra
    python tools/wa-to-md.py export/World-Talan-97c    worldanvil-export/Talan
"""

import json
import os
import re
import sys


# ---------------------------------------------------------------------------
# BBCode → Markdown
# ---------------------------------------------------------------------------

def bbcode_to_md(text: str) -> str:
    if not text:
        return ""

    # Headings with optional UUID: [h1|uuid]...[/h1]
    text = re.sub(r'\[h1(?:\|[^\]]+)?\](.*?)\[/h1\]', r'# \1', text, flags=re.DOTALL)
    text = re.sub(r'\[h2(?:\|[^\]]+)?\](.*?)\[/h2\]', r'## \1', text, flags=re.DOTALL)
    text = re.sub(r'\[h3(?:\|[^\]]+)?\](.*?)\[/h3\]', r'### \1', text, flags=re.DOTALL)
    text = re.sub(r'\[h4(?:\|[^\]]+)?\](.*?)\[/h4\]', r'#### \1', text, flags=re.DOTALL)

    # Inline formatting
    text = re.sub(r'\[b\](.*?)\[/b\]', r'**\1**', text, flags=re.DOTALL)
    text = re.sub(r'\[i\](.*?)\[/i\]', r'*\1*', text, flags=re.DOTALL)
    text = re.sub(r'\[u\](.*?)\[/u\]', r'<u>\1</u>', text, flags=re.DOTALL)
    text = re.sub(r'\[s\](.*?)\[/s\]', r'~~\1~~', text, flags=re.DOTALL)

    # Tables — convert before paragraphs
    text = convert_tables(text)

    # Block containers (just strip the tags, keep content)
    text = re.sub(r'\[(?:ul|ol|li)\]', '', text)
    text = re.sub(r'\[/(?:ul|ol|li)\]', '', text)

    # Sub-bullets: leading "--" → "  -"
    text = re.sub(r'(?m)^-- ', '  - ', text)

    # Paragraphs
    text = re.sub(r'\[p\](.*?)\[/p\]', lambda m: m.group(1).strip() + '\n', text, flags=re.DOTALL)

    # Horizontal rule
    text = re.sub(r'\[hr\]', '\n---\n', text)

    # Line break
    text = re.sub(r'\[br\]', '\n', text)

    # Links [url:text] or [url=...|text]
    text = re.sub(r'\[url=([^\]|]+)\|([^\]]+)\]', r'[\2](\1)', text)
    text = re.sub(r'\[url\](.*?)\[/url\]', r'\1', text, flags=re.DOTALL)

    # Images — just drop them (no local copies)
    text = re.sub(r'\[img[^\]]*\].*?\[/img\]', '', text, flags=re.DOTALL)

    # Quotes / blockquotes
    text = re.sub(r'\[quote\](.*?)\[/quote\]', lambda m: '\n> ' + m.group(1).strip().replace('\n', '\n> ') + '\n', text, flags=re.DOTALL)

    # Remove any remaining unknown BBCode tags
    text = re.sub(r'\[[^\]]+\]', '', text)

    # Collapse 3+ blank lines to 2
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text.strip()


def convert_tables(text: str) -> str:
    """Convert [table][tr][th/td]...[/table] blocks to Markdown tables."""
    def render_table(match):
        block = match.group(1)
        rows = re.findall(r'\[tr\](.*?)\[/tr\]', block, re.DOTALL)
        if not rows:
            return ''
        md_rows = []
        header_done = False
        for row in rows:
            # Find th or td cells
            cells = re.findall(r'\[(?:th|td)\](.*?)\[/(?:th|td)\]', row, re.DOTALL)
            cells = [bbcode_to_md(c).strip().replace('\n', ' ') for c in cells]
            is_header = bool(re.search(r'\[th\]', row))
            md_rows.append('| ' + ' | '.join(cells) + ' |')
            if is_header and not header_done:
                md_rows.append('| ' + ' | '.join(['---'] * len(cells)) + ' |')
                header_done = True
        # If no header row was found, insert separator after first row
        if not header_done and md_rows:
            first_pipe_count = md_rows[0].count('|') - 1
            md_rows.insert(1, '| ' + ' | '.join(['---'] * first_pipe_count) + ' |')
        return '\n' + '\n'.join(md_rows) + '\n'

    return re.sub(r'\[table\](.*?)\[/table\]', render_table, text, flags=re.DOTALL)


# ---------------------------------------------------------------------------
# Metadata helpers
# ---------------------------------------------------------------------------

SKIP_FIELDS = {
    'id', 'slug', 'icon', 'url', 'subscribergroups', 'folderId', 'tags',
    'updateDate', 'creationDate', 'publicationDate', 'notificationDate',
    'position', 'excerpt', 'wordcount', 'likes', 'views', 'userMetadata',
    'articleMetadata', 'cssClasses', 'displayCss', 'customArticleTemplate',
    'editor', 'author', 'world', 'articleParent', 'cover', 'coverSource',
    'seeded', 'displaySidebar', 'articleNext', 'articlePrevious', 'timeline',
    'prompt', 'gallery', 'block', 'orgchart', 'showSeeded', 'webhookUpdate',
    'communityUpdate', 'commentPlaceholder', 'passcodecta', 'metaTitle',
    'metaDescription', 'coverIsMap', 'isFeaturedArticle', 'isAdultContent',
    'isLocked', 'allowComments', 'allowContentCopy', 'showInToc',
    'isEmphasized', 'displayAuthor', 'displayChildrenUnder', 'displayTitle',
    'displaySheet', 'badge', 'editURL', 'isEditable', 'success',
    'content', 'title', 'state', 'isWip', 'isDraft', 'entityClass',
    'templateType', 'category', 'portrait', 'flag',
    # GGM fields (game master module, rarely used)
    *[f for f in [] if f.startswith('ggm')],
}

FIELD_LABELS = {
    'pronunciation': 'Pronunciation',
    'snippet': 'Snippet',
    'subheading': 'Subheading',
    'sidebarcontent': 'Sidebar',
    'sidepanelcontenttop': 'Side Panel (top)',
    'sidepanelcontent': 'Side Panel',
    'sidebarcontentbottom': 'Sidebar (bottom)',
    'footnotes': 'Footnotes',
    'fullfooter': 'Footer',
    'authornotes': 'Author Notes',
    'scrapbook': 'Scrapbook',
    'credits': 'Credits',
    # Person
    'firstname': 'First Name', 'lastname': 'Last Name', 'middlename': 'Middle Name',
    'maidenname': 'Maiden Name', 'nickname': 'Nickname', 'honorific': 'Honorific',
    'suffix': 'Suffix', 'pronouns': 'Pronouns', 'gender': 'Gender',
    'genderidentity': 'Gender Identity', 'sex': 'Sex', 'sexuality': 'Sexuality',
    'age': 'Age', 'dob': 'Date of Birth', 'dobDisplay': 'Birth Display',
    'dod': 'Date of Death', 'dodDisplay': 'Death Display',
    'circumstancesBirth': 'Circumstances of Birth', 'circumstancesDeath': 'Circumstances of Death',
    'eyes': 'Eyes', 'hair': 'Hair', 'skin': 'Skin', 'height': 'Height', 'weight': 'Weight',
    'physique': 'Physique', 'bodyFeatures': 'Body Features', 'facialFeatures': 'Facial Features',
    'identifyingCharacteristics': 'Identifying Characteristics', 'clothing': 'Clothing',
    'items': 'Items', 'specialAbilities': 'Special Abilities',
    'currentstatus': 'Current Status', 'history': 'History', 'employment': 'Employment',
    'achievements': 'Achievements', 'failures': 'Failures', 'mentalTraumas': 'Mental Traumas',
    'intellectualCharacteristics': 'Intellectual Characteristics', 'morality': 'Morality',
    'taboos': 'Taboos', 'education': 'Education', 'languages': 'Languages',
    'quotes': 'Quotes', 'motivation': 'Motivation', 'virtues': 'Virtues', 'vices': 'Vices',
    'quirksPersonality': 'Personality Quirks', 'quirksPhysical': 'Physical Quirks',
    'hygiene': 'Hygiene', 'speech': 'Speech', 'mannerisms': 'Mannerisms',
    'hobbies': 'Hobbies', 'wealth': 'Wealth', 'socialAptitude': 'Social Aptitude',
    'savviesIneptitudes': 'Savvies & Ineptitudes', 'likesDislikes': 'Likes & Dislikes',
    'relations': 'Relations', 'family': 'Family', 'religion': 'Religion',
    'titles': 'Titles', 'representationLegacy': 'Legacy',
    'presentation': 'Presentation', 'perceptionPhysical': 'Physical Perception',
    # Organization
    'motto': 'Motto', 'publicAgenda': 'Public Agenda', 'alternativeNames': 'Alternative Names',
    'demonym': 'Demonym', 'assets': 'Assets', 'structure': 'Structure',
    'disbandment': 'Disbandment', 'demographics': 'Demographics',
    'veterancy': 'Veterancy', 'trainingLevel': 'Training Level',
    'governmentsystem': 'Government System', 'powerstructure': 'Power Structure',
    'economicsystem': 'Economic System', 'legislative': 'Legislative',
    'judicial': 'Judicial', 'executive': 'Executive', 'gazetteer': 'Gazetteer',
    'currency': 'Currency', 'territory': 'Territory', 'military': 'Military',
    'technology': 'Technology', 'foreignrelations': 'Foreign Relations',
    'laws': 'Laws', 'culture': 'Culture', 'imports': 'Imports', 'exports': 'Exports',
    'agricultureAndIndustry': 'Agriculture & Industry', 'tradeAndTransport': 'Trade & Transport',
    'education': 'Education', 'infrastructure': 'Infrastructure',
    'mythos': 'Mythos', 'origins': 'Origins', 'cosmology': 'Cosmology',
    'tenets': 'Tenets', 'priesthood': 'Priesthood', 'ethics': 'Ethics',
    'divinepowers': 'Divine Powers', 'intrigue': 'Intrigue', 'worship': 'Worship',
    'sects': 'Sects', 'foundingDate': 'Founded', 'dissolutionDate': 'Dissolved',
    # Location / Landmark / Settlement
    'geography': 'Geography', 'naturalresources': 'Natural Resources',
    'population': 'Population', 'areaSize': 'Area', 'defences': 'Defences',
    'guilds': 'Guilds', 'tourism': 'Tourism', 'industry': 'Industry',
    'architecture': 'Architecture', 'government': 'Government',
    'constructed': 'Constructed', 'ruined': 'Ruined',
    'florafauna': 'Flora & Fauna', 'ecosystem': 'Ecosystem',
    'ecosystemCycles': 'Ecosystem Cycles', 'localizedPhenomena': 'Localized Phenomena',
    'climate': 'Climate', 'alterations': 'Alterations', 'purpose': 'Purpose',
    'design': 'Design', 'entries': 'Entries', 'denizens': 'Denizens',
    'valuables': 'Valuables', 'hazards': 'Hazards', 'effects': 'Effects',
    'sensory': 'Sensory', 'properties': 'Properties', 'contents': 'Contents',
    'pointOfInterest': 'Points of Interest', 'district': 'District',
    # Species
    'trinominal': 'Trinominal', 'ancenstry': 'Ancestry', 'lifespan': 'Lifespan',
    'anatomy': 'Anatomy', 'perception': 'Perception', 'genetics': 'Genetics',
    'ecology': 'Ecology', 'diet': 'Diet', 'domestication': 'Domestication',
    'uses': 'Uses', 'biocycle': 'Biological Cycle', 'growthrate': 'Growth Rate',
    'symbiotic': 'Symbiotic Relationships', 'isSentient': 'Sentient',
    'isIntelligent': 'Intelligent', 'geographicalOrigin': 'Geographic Origin',
    'averageIntelligence': 'Average Intelligence', 'averagePhysique': 'Average Physique',
    'facialCharacteristics': 'Facial Characteristics', 'skinHairColor': 'Skin/Hair Colour',
    'traits': 'Traits', 'averageHeight': 'Average Height', 'averageWeight': 'Average Weight',
    'averageLength': 'Average Length', 'namingTraditions': 'Naming Traditions',
    'firstnamesMale': 'Male Names', 'firstnamesFemale': 'Female Names', 'lastnames': 'Last Names',
    'majorReligions': 'Major Religions', 'majorOrganizations': 'Major Organizations',
    'beautyIdeals': 'Beauty Ideals', 'genderIdeals': 'Gender Ideals',
    'courtshipIdeals': 'Courtship Ideals', 'relationshipsIdeals': 'Relationship Ideals',
    'technologicalLevel': 'Technological Level', 'etiquette': 'Etiquette',
    'dresscode': 'Dress Code', 'customs': 'Customs', 'socialstructure': 'Social Structure',
    'mythsAndLegends': 'Myths & Legends', 'historicalFigures': 'Historical Figures',
    'interspeciesRelations': 'Interspecies Relations', 'isExtinct': 'Extinct',
    'conservation': 'Conservation Status', 'behaviour': 'Behaviour',
    # Rank
    'alternativeTitle': 'Alternative Title', 'lengthOfTerm': 'Length of Term',
    'duties': 'Duties', 'qualifications': 'Qualifications', 'requirements': 'Requirements',
    'appointment': 'Appointment', 'heredity': 'Heredity', 'responsibilities': 'Responsibilities',
    'culturalSignificance': 'Cultural Significance', 'notableHolders': 'Notable Holders',
    'benefits': 'Benefits', 'removal': 'Removal', 'equatesTo': 'Equates To',
    'equipment': 'Equipment', 'heraldry': 'Heraldry', 'rankCreation': 'Creation',
    'rankStatus': 'Status', 'authoritySource': 'Authority Source', 'formofaddress': 'Form of Address',
    # Myth
    'summary': 'Summary', 'historicalbasis': 'Historical Basis', 'spread': 'Spread',
    'variations': 'Variations', 'culturalreception': 'Cultural Reception',
    'literature': 'Literature', 'art': 'Art', 'dateofsetting': 'Date of Setting',
    'dateofrecording': 'Date of Recording', 'telling': 'Telling',
    # Ritual
    'components': 'Components', 'execution': 'Execution', 'participants': 'Participants',
    'observance': 'Observance', 'location': 'Location',
}


def render_field(key, value):
    """Render a single non-null structured field as a markdown section."""
    if value is None:
        return ''
    label = FIELD_LABELS.get(key, key.replace('_', ' ').title())

    # Boolean
    if isinstance(value, bool):
        return f'**{label}:** {"Yes" if value else "No"}\n\n'

    # Object with a title
    if isinstance(value, dict):
        title = value.get('title') or value.get('name') or str(value)
        return f'**{label}:** {title}\n\n'

    val_str = str(value).strip()
    if not val_str:
        return ''

    converted = bbcode_to_md(val_str)
    if '\n' in converted:
        return f'### {label}\n\n{converted}\n\n'
    else:
        return f'**{label}:** {converted}\n\n'


# ---------------------------------------------------------------------------
# Main converter
# ---------------------------------------------------------------------------

def slug_to_filename(title: str) -> str:
    """Turn an article title into a safe filename."""
    name = title.lower()
    name = re.sub(r"[^\w\s-]", '', name)
    name = re.sub(r'[\s_]+', '-', name).strip('-')
    return name + '.md'


def convert_article(data: dict) -> str:
    title = data.get('title', 'Untitled')
    entity_class = data.get('entityClass', '')
    template = data.get('templateType', '')
    category = (data.get('category') or {}).get('title', '')
    updated = (data.get('updateDate') or {}).get('date', '')[:10]
    wip = data.get('isWip', False)
    draft = data.get('isDraft', False)

    status_parts = []
    if draft:
        status_parts.append('Draft')
    if wip:
        status_parts.append('WIP')
    status = ' · '.join(status_parts) if status_parts else 'Published'

    type_label = template.title() if template else entity_class

    lines = []
    lines.append(f'# {title}\n')
    lines.append(f'**Type:** {type_label}  ')
    if category:
        lines.append(f'**Category:** {category}  ')
    lines.append(f'**Status:** {status}  ')
    if updated:
        lines.append(f'**Updated:** {updated}')
    lines.append('\n---\n')

    # Main content
    content = data.get('content') or ''
    if content.strip():
        lines.append(bbcode_to_md(content))
        lines.append('')

    # Structured fields — only render non-null ones not in skip list
    extra_sections = []
    for key, value in data.items():
        if key in SKIP_FIELDS:
            continue
        if key.startswith('ggm'):
            continue
        if value is None or value == '' or value == []:
            continue
        rendered = render_field(key, value)
        if rendered:
            extra_sections.append(rendered)

    if extra_sections:
        lines.append('\n---\n')
        lines.extend(extra_sections)

    return '\n'.join(lines)


def process_world(export_dir: str, output_dir: str):
    articles_dir = os.path.join(export_dir, 'articles')
    if not os.path.isdir(articles_dir):
        print(f'No articles/ folder found in {export_dir}')
        return

    files = [f for f in os.listdir(articles_dir) if f.endswith('.json')]
    print(f'Converting {len(files)} articles from {export_dir}...')

    converted = 0
    for fname in files:
        path = os.path.join(articles_dir, fname)
        with open(path, encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                print(f'  SKIP (bad JSON): {fname} — {e}')
                continue

        category = (data.get('category') or {}).get('title', '')
        if category:
            out_folder = os.path.join(output_dir, category)
        else:
            out_folder = output_dir

        os.makedirs(out_folder, exist_ok=True)

        out_filename = slug_to_filename(data.get('title', fname[:-5]))
        out_path = os.path.join(out_folder, out_filename)

        md = convert_article(data)
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(md)

        converted += 1

    print(f'Done. {converted} files written to {output_dir}')


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)

    export_dir = sys.argv[1]
    output_dir = sys.argv[2]

    if not os.path.isdir(export_dir):
        print(f'Export dir not found: {export_dir}')
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)
    process_world(export_dir, output_dir)


if __name__ == '__main__':
    main()
