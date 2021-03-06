from typing import Optional, List
from datetime import datetime

import strawberry

from felicity.gql import PageInfo
from felicity.gql.analysis.types.analysis import SampleType, AnalysisType, QCSetType
from felicity.gql.setup.types import MethodType, InstrumentType
from felicity.gql.user.types import UserType


@strawberry.type
class AnalysisResultType:
    uid: int
    sample_uid: int
    sample: SampleType
    worksheet_uid: Optional[int]
    worksheet_position: Optional[int]
    assigned: bool
    analysis_uid: Optional[int]
    analysis: Optional[AnalysisType]
    instrument_uid: Optional[int]
    instrument: Optional[InstrumentType]
    method_uid: Optional[int]
    method: Optional[MethodType]
    result: Optional[str]
    analyst_uid: Optional[int]
    submitted_by_uid: Optional[int]
    date_submitted: Optional[datetime]
    verified_by_uid: Optional[int]
    date_verified: Optional[datetime]
    invalidated_by_uid: Optional[int]
    date_invalidated: datetime
    retest: bool
    parent_id: int
    parent: Optional['AnalysisResultType']
    reportable: bool
    status: Optional[str]
    created_by_uid: Optional[int]
    created_by: Optional[UserType]
    created_at: Optional[datetime]
    updated_by_uid: Optional[int]
    updated_by: Optional[UserType]
    updated_at: Optional[datetime]


@strawberry.type
class SamplesWithResults(SampleType):
    analysis_results: Optional[List[AnalysisResultType]]


@strawberry.type
class SampleEdge:
    cursor: str
    node: SamplesWithResults


@strawberry.type
class SampleCursorPage:
    page_info: PageInfo
    edges: Optional[List[SampleEdge]]
    items: Optional[List[SamplesWithResults]]
    total_count: int


@strawberry.type
class QCSetWithSamples(QCSetType):
    samples: Optional[List[SamplesWithResults]]


@strawberry.type
class QCSetEdge:
    cursor: str
    node: QCSetWithSamples


@strawberry.type
class QCSetCursorPage:
    page_info: PageInfo
    edges: Optional[List[QCSetEdge]]
    items: Optional[List[QCSetWithSamples]]
    total_count: int
