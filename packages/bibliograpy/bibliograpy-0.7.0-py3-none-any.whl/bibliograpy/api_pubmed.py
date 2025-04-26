"""
Pubmed specification model.
"""
from dataclasses import dataclass
from enum import Enum, auto

from bibliograpy.api_mesh import MeshPublicationType
from bibliograpy.bibliography import PUBMED_FORMAT
from bibliograpy.api_bibtex import _cite


@dataclass(frozen=True)
class Tag:
    """A field tag."""
    auto: auto
    repeating: bool = False

@_cite(PUBMED_FORMAT)
class Tags(Tag, Enum):
    """
    Pubmed fields.
    """

    AB = auto()
    """Abstract 	
    
    English language abstract taken directly from the published article"""

    AD = auto()
    """Affiliation
    
    Author or corporate author addresses"""

    AID = auto()
    """Article Identifier
    
    Article ID values supplied by the publisher may include the pii (controlled publisher identifier), doi (digital 
    object identifier), or book accession"""

    AU = (auto(), True)
    """Author
    
    Authors"""

    AUID = auto()
    """Author Identifier
    
    Unique identifier associated with an author, corporate author, or investigator name"""

    BTI = auto()
    """Book Title
    
    Book Title"""

    CI = auto()
    """Copyright Information
    
    Copyright statement provided by the publisher"""

    CIN = auto()
    """Comment In
    
    Reference containing a comment about the article"""

    CN = auto()
    """Corporate Author
    
    Corporate author or group names with authorship responsibility"""

    COI = auto()
    """Conflict of Interest
    
    Conflict of interest statement"""

    CON = auto()
    """Comment On
    
    Reference upon which the article comments"""

    CP = auto()
    """Chapter
    
    Book chapter"""

    CRDT = auto()
    """Create Date
    
    The date the citation record was first created"""

    CRF = auto()
    """Corrected and republished from
    
    Final, correct version of an article"""

    CRI = auto()
    """Corrected and republished in
    
    Original article that was republished in corrected form"""

    CTDT = auto()
    """Contribution Date
    
    Book contribution date"""

    CTI = auto()
    """Collection Title
    
    Collection Title"""

    DCOM = auto()
    """Completion Date
    
    NLM internal processing completion date"""

    DDIN = auto()
    """Dataset described in
    
    Citation for the primary article resulting from a dataset"""

    DRIN = auto()
    """Dataset use reported in
    
    Citation for an article that uses a dataset from another scientific article"""

    DEP = auto()
    """Date of Electronic Publication
    
    Electronic publication date"""

    DP = auto()
    """Publication Date
    
    The date the article was published"""

    DRDT = auto()
    """Date Revised
    
    Book Revision Date"""

    ECF = auto()
    """Expression of Concern For
    
    Reference containing an expression of concern for an article"""

    ECI = auto()
    """Expression of Concern In
    
    Cites the original article for which there is an expression of concern"""

    EDAT = auto()
    """Entry Date
    
    The date the citation was added to PubMed; the date is set to the publication date if added more than 1 year after 
    the date published"""

    EFR = auto()
    """Erratum For
    
    Cites the original article for which there is a published erratum; as of 2016, partial retractions are considered 
    errata """

    EIN = auto()
    """Erratum In
    
    Cites a published erratum to the article"""

    ED = auto()
    """Editor
    
    Book editors"""

    EN = auto()
    """Edition
    
    Book edition"""

    FAU = auto()
    """Full Author Name
    
    Full author names"""

    FED = auto()
    """Full Editor Name
    
    Full editor names"""

    FIR = auto()
    """Full Investigator Name
    
    Full investigator or collaborator names"""

    FPS = auto()
    """Full Personal Name as Subject
    
    Full Personal Name of the subject of the article"""

    GN = auto()
    """General Note
    
    Supplemental or descriptive information related to the document"""

    GR = auto()
    """Grants and Funding
    
    Grant numbers, contract numbers, and intramural research identifiers associated with a publication"""

    GS = auto()
    """Gene Symbol
    
    Abbreviated gene names (used 1991 through 1996)"""

    IP = auto()
    """Issue
    
    The number of the issue, part, or supplement of the journal in which the article was published"""

    IR = auto()
    """Investigator
    
    Investigator or collaborator"""

    IRAD = auto()
    """Investigator Affiliation
    
    Investigator or collaborator addresses"""

    IS = auto()
    """ISSN
    
    International Standard Serial Number of the journal"""

    ISBN = auto()
    """ISBN
    
    International Standard Book Number"""

    JID = auto()
    """NLM Unique ID
    
    Unique journal ID in the NLM catalog of books, journals, and audiovisuals"""

    JT = auto()
    """Full Journal Title
    
    Full journal title from NLM cataloging data"""

    LA = auto()
    """Language
    
    The language in which the article was published"""

    LID = auto()
    """Location ID
    
    The pii or doi that serves the role of pagination"""

    LR = auto()
    """Modification Date
    
    Citation last revision date"""

    MH = (auto(), True)
    """MeSH Terms
    
    NLM Medical Subject Headings (MeSH) controlled vocabulary"""

    MHDA = auto()
    """MeSH Date
    
    The date MeSH terms were added to the citation. The MeSH date is the same as the Entrez date until MeSH are added"""

    MID = auto()
    """Manuscript Identifier
    
    Identifier assigned to an author manuscript submitted to the NIH Manuscript Submission System"""

    NM = auto()
    """Substance Name
    
    Supplementary Concept Record (SCR) data"""

    OAB = auto()
    """Other Abstract
    
    Abstract supplied by an NLM collaborating organization"""

    OABL = auto()
    """Other Abstract Language
    
    Language of an abstract available from the publisher"""

    OCI = auto()
    """Other Copyright Information
    
    Copyright owner"""

    OID = auto()
    """Other ID
    
    Identification numbers provided by organizations supplying citation data"""

    ORI = auto()
    """Original Report In
    
    Cites the original article associated with the patient summary"""

    OT = auto()
    """Other Term
    
    Non-MeSH subject terms (keywords) either assigned by an organization identified by the Other Term Owner, or 
    generated by the author and submitted by the publisher"""

    OTO = auto()
    """Other Term Owner
    
    Organization that may have provided the Other Term data"""

    OWN = auto()
    """Owner
    
    Organization acronym that supplied citation data"""

    PB = auto()
    """Publisher
    
    Publishers of Books & Documents citations"""

    PG = auto()
    """Pagination
    
    The full pagination of the article"""

    PHST = auto()
    """Publication History Status Date
    
    Publisher supplied dates regarding the article publishing process and PubMed date stamps:
        
        received: manuscript received for review
        revised: manuscript revised by publisher or author
        accepted: manuscript accepted for publication
        aheadofprint: published electronically prior to final publication
        entrez: PubMed Create Date [crdt]
        pubmed: PubMed Entry Date [edat]
        medline: PubMed MeSH Date [mhda]"""

    PL = auto()
    """Place of Publication
    
    Journal's (country only) or book’s place of publication"""

    PMC = auto()
    """PubMed Central Identifier
    
    Unique identifier for the cited article in PubMed Central (PMC)"""

    PMCR = auto()
    """PMC Release
    
    Availability of PMC article"""

    PMID = auto()
    """PubMed Unique Identifier
    
    Unique number assigned to each PubMed citation"""

    PS = auto()
    """Personal Name as Subject
    
    Individual is the subject of the article"""

    PST = auto()
    """Publication Status
    
    Publication status"""

    PT = (auto(), True) #  seems to be repeatable as seen in downloaded examples on the internet
    """Publication Type
    
    The type of material the article represents"""

    RF = auto()
    """Number of References
    
    Number of bibliographic references for Review articles"""

    RIN = auto()
    """Retraction In
    
    Retraction of the article"""

    RN = (auto(), True)
    """EC/RN Number
    
    Includes chemical, protocol or disease terms. May also include a number assigned by the Enzyme Commission or by the 
    Chemical Abstracts Service."""

    ROF = auto()
    """Retraction Of
    
    Article being retracted"""

    RPF = auto()
    """Republished From
    
    Article being cited has been republished or reprinted in either full or abridged form from another source"""

    RPI = auto()
    """Republished In
    
    Article being cited also appears in another source in either full or abridged form"""

    RRI = auto()
    """Retracted and Republished In
    
    Final, republished version of an article"""

    RRF = auto()
    """Retracted and Republished From
    
    Original article that was retracted and republished"""

    SB = auto()
    """Subset
    
    Journal or citation subset values representing specialized topics"""

    SFM = auto()
    """Space Flight Mission
    
    NASA-supplied data space flight/mission name and/or number"""

    SI = auto()
    """Secondary Source ID
    
    Identifies secondary source databanks and accession numbers of molecular sequences discussed in articles"""

    SO = auto()
    """Source
    
    Composite field containing bibliographic information"""

    SPIN = auto()
    """Summary For Patients In
    
    Cites a patient summary article"""

    STAT = auto()
    """Status Tag
    
    Used for internal processing at NLM"""

    TA = auto()
    """Journal Title Abbreviation
    
    Standard journal title abbreviation"""

    TI = auto()
    """Title
    
    The title of the article"""

    TT = auto()
    """Transliterated Title
    
    Title of the article originally published in a non-English language, in that language"""

    UIN = auto()
    """Update In
    
    Update to the article"""

    UOF = auto()
    """Update Of
    
    The article being updated"""

    VI = auto()
    """Volume
    
    Volume number of the journal"""

    VTI = auto()
    """Volume Title
    
Book Volume Title"""

    @staticmethod
    def parse(tag_str: str):
        """Parses a tag name into an enum value."""
        for n in Tags:
            if tag_str == n.name:
                return n
        raise ValueError(f'unknown {tag_str} tag')


def default_pubmed_formatter(r: dict[Tags, str | list[str] | MeshPublicationType]):
    """The default formatter for PubMed references."""
    title = ''
    if Tags.TI in r:
        title = r[Tags.TI]

    ref_id = ''
    if Tags.PMID in r:
        ref_id = r[Tags.PMID]
    if Tags.PMC in r:
        ref_id = r[Tags.PMC]
    if Tags.OID in r:
        ref_id = r[Tags.OID]
    if Tags.AID in r:
        ref_id = r[Tags.AID]
    if Tags.MID in r:
        ref_id = r[Tags.MID]
    return f'{title} [{ref_id}]'
