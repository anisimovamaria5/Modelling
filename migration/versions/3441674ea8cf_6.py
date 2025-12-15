from typing import Sequence, Union

from alembic import op
import pandas as pd
import sqlalchemy as sa

from app_name.models.models_gdh import UOM, Dimension


# revision identifiers, used by Alembic.
revision: str = '3441674ea8cf'
down_revision: Union[str, None] = '890d03491bc3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    session = sa.orm.Session(bind=bind)

    dimen_dct = {}
    df_1 = pd.read_excel('media/Dimen.xlsx', sheet_name='dimen')
    for _, row in df_1.iterrows():
        dimen = Dimension(
            name=row['name'],
            dimen=row['dimen']
        )
        session.add(dimen) 
        session.flush()   
        dimen_dct[row['dimen']] = dimen

    df_2 = pd.read_excel('media/Dimen.xlsx', sheet_name='uom')
    for _, row in df_2.iterrows():
        
        dimen_id = None
        if not pd.isna(row['dimen']):
            dimen = dimen_dct.get(row['dimen'])
            dimen_id = dimen.id if dimen else None

        uom = UOM(
            uom_code=row['uon_code'],
            name=row['name'],
            short_name=row['short_name'],
            dimen_id=dimen_id
        )
        session.add(uom)

    session.commit()
    session.close()


def downgrade() -> None:
    bind = op.get_bind()
    session = sa.orm.Session(bind=bind)

    session.query(Dimension).delete()
    session.query(UOM).delete()
    session.commit()
    session.close()
