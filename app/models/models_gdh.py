from sqlalchemy import Column, String, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.base import BaseMethods
from app.database import Base


class EqCompressorTypePressureOut(BaseMethods):
    __tablename__ = 'EQ_COMPRESSOR_TYPE_PRESSURE_OUT'
    __table_args__ = {'comment':'Таблица номинальных значений выходных давлений'}

    id = Column(Integer, primary_key=True)
    value = Column(Float)

    eq_compressor_type = relationship('EqCompressorType', 
                                      back_populates='EQ_COMPRESSOR_TYPE_PRESSURE_OUT',
                                      cascade="all, delete-orphan", lazy="selectin")


class EqCompressorTypeCompRatio(BaseMethods):
    __tablename__ = 'EQ_COMPRESSOR_TYPE_COMP_RATIO'
    __table_args__ = {'comment':'Таблица номинальных значений степеней сжатия'}

    id = Column(Integer, primary_key=True)
    value = Column(Float)

    eq_compressor_type = relationship('EqCompressorType', 
                                    back_populates='EQ_COMPRESSOR_TYPE_COMP_RATIO',
                                    cascade="all, delete-orphan", lazy="selectin")


class EqCompressorTypeFreqNomimal(BaseMethods):
    __tablename__ = 'EQ_COMPRESSOR_TYPE_FREQ_NOMINAL'
    __table_args__ = {'comment':'Таблица номинальных значений частот'}


    id = Column(Integer, primary_key=True)
    value = Column(Float)    

    eq_compressor_type = relationship('EqCompressorType', 
                                      back_populates='EQ_COMPRESSOR_TYPE_FREQ_NOMINAL',
                                      cascade="all, delete-orphan", lazy="selectin")


class EqCompressorTypePower(BaseMethods):
    __tablename__ = 'EQ_COMPRESSOR_TYPE_POWER'
    __table_args__ = {'comment':'Таблица номинальных значений мощностей'}


    id = Column(Integer, primary_key=True)
    value = Column(Float)      

    eq_compressor_type = relationship('EqCompressorType', 
                                      back_populates='EQ_COMPRESSOR_TYPE_POWER',
                                      cascade="all, delete-orphan", lazy="selectin")
    

class EqCompressorType(BaseMethods):
    """_summary_

    Args:
        Base (_type_): _description_
    """
    __tablename__ = 'EQ_COMPRESSOR_TYPE'
    __table_args__ = {'comment':'Таблица номиналов СПЧ'}


    id = Column(Integer, primary_key=True)

    press_out_id = Column(Integer, ForeignKey('EQ_COMPRESSOR_TYPE_PRESSURE_OUT.id'))
    comp_ratio_id = Column(Integer, ForeignKey('EQ_COMPRESSOR_TYPE_COMP_RATIO.id'))
    freq_nominal_id = Column(Integer, ForeignKey('EQ_COMPRESSOR_TYPE_FREQ_NOMINAL.id'))
    power_id = Column(Integer, ForeignKey('EQ_COMPRESSOR_TYPE_POWER.id'))

    eq_compressor_type_pressure_out = relationship('EqCompressorTypePressureOut', 
                                      back_populates='EQ_COMPRESSOR_TYPE')    
    eq_compressor_type_comp_ratio = relationship('EqCompressorTypeCompRatio', 
                                      back_populates='EQ_COMPRESSOR_TYPE')    
    eq_compressor_type_freq_nominal = relationship('EqCompressorTypeFreqNomimal', 
                                    back_populates='EQ_COMPRESSOR_TYPE')    
    eq_compressor_type_power = relationship('EqCompressorTypePower', 
                                    back_populates='EQ_COMPRESSOR_TYPE')     
    eq_compressor_unit = relationship('EqCompressorUnit', 
                                back_populates='EQ_COMPRESSOR_TYPE',
                                cascade="all, delete-orphan", lazy="selectin")        


class UOM(BaseMethods):
    __tablename__ = 'UOM'
    __table_args__ = {'comment':'Таблица размерностей'}


    id = Column(Integer, primary_key=True)
    uom_code = Column(String, comment='Код размерности')      

    eq_compressor_type = relationship('EqCompressorPerfomanceCurveParam', 
                                      back_populates='UOM',
                                      cascade="all, delete-orphan", lazy="selectin")
    calc_comp_param = relationship('CalcCompParam', 
                                    back_populates='UOM',
                                    cascade="all, delete-orphan", lazy="selectin")
    



class EqCompressorPerfomanceCurveParam(BaseMethods):
    __tablename__ = 'EQ_COMPRESSSOR_PERFORMANCE_CURVE_PARAM'
    __table_args__ = {'comment':'Таблица макропараметров ГДХ'}


    id = Column(Integer, primary_key=True)
    name = Column(String, comment='Имя параметра')
    value = Column(Float)

    uom_id = Column(Integer, ForeignKey('UOM.id'))
    unit_id = Column(Integer, ForeignKey('EQ_COMPRESSSOR_UNIT.id'))

    uom = relationship('UOM',
                       back_populates='EQ_COMPRESSSOR_PERFORMANCE_CURVE_PARAM')
    unit = relationship('EqCompressorUnit',
                       back_populates='EQ_COMPRESSSOR_PERFORMANCE_CURVE_PARAM')


class EqCompressorPerfomanceCurve(BaseMethods):
    __tablename__ = 'EQ_COMPRESSSOR_PERFORMANCE_CURVE'
    __table_args__ = {'comment':'Таблица безразмерных параметров'}


    id = Column(Integer, primary_key=True)
    head = Column(Float, comment='Коэффициент напора')
    non_dim_rate = Column(Float, comment='Коэффициент расхода')
    kpd = Column(Float, comment='Кпд')

    unit_id = Column(Integer, ForeignKey('EQ_COMPRESSSOR_UNIT.id'))
    param_id = Column(Integer, ForeignKey('CALC_COMP_PARAMS.id'))

    calc_comp_param = relationship('CalcCompParam',
                         back_populates='EQ_COMPRESSSOR_PERFORMANCE_CURVE')
    unit = relationship('EqCompressorUnit',
                         back_populates='EQ_COMPRESSSOR_PERFORMANCE_CURVE')


class EqCompressorUnit(BaseMethods):
    __tablename__ = 'EQ_COMPRESSSOR_UNIT'
    __table_args__ = {'comment':'Таблица - сущность ГДХ/компрессор'}


    id = Column(Integer, primary_key=True)
    unique_name = Column(String, comment='Уникальное имя ГДХ')

    # field_id = Column(Integer, ForeignKey('FIELD.id'))
    type_id = Column(Integer, ForeignKey('EQ_COMPRESSOR_TYPE.id'))
    dks_id = Column(Integer, ForeignKey('DKS.id'))


    param = relationship('EqCompressorPerfomanceCurveParam',
                         back_populates='EQ_COMPRESSSOR_UNIT',
                         cascade="all, delete-orphan", lazy="selectin")
    type = relationship('EqCompressorType',
                         back_populates='EQ_COMPRESSSOR_UNIT')
    # field = relationship('Field',
    #                     back_populates='EQ_COMPRESSSOR_UNIT')    
    curve = relationship('EqCompressorPerfomanceCurve',
                        back_populates='EQ_COMPRESSSOR_UNIT',
                         cascade="all, delete-orphan", lazy="selectin")
    dks = relationship('Dks',
                         back_populates='EQ_COMPRESSSOR_UNIT')
    

class CalcCompParam(BaseMethods):
    __tablename__ = 'CALC_COMP_PARAMS'
    __table_args__ = {'comment':'Таблица дефолтных параметров расчета'}


    id = Column(Integer, primary_key=True)
    name = Column(String)
    value = Column(Float)

    uom_id = Column(Integer, ForeignKey('UOM.id'))

    curve = relationship('EqCompressorPerfomanceCurve',
                         back_populates='CALC_COMP_PARAMS',
                         cascade="all, delete-orphan", lazy="selectin")
    uom = relationship('UOM',
                         back_populates='CALC_COMP_PARAMS')


class Field(BaseMethods):
    __tablename__ = 'FIELD'
    __table_args__ = {'comment':'Таблица месторождений'}


    id = Column(Integer, primary_key=True)
    name = Column(String, comment='Название месторождения') 

    companies_id = Column(Integer, ForeignKey('COMPANIES.id'))   

    # eq_compressor_type = relationship('EqCompressorUnit', 
    #                                   back_populates='FIELD',
    #                                   cascade="all, delete-orphan", lazy="selectin")
    companies = relationship('Companies', 
                            back_populates='FIELD')
    dks = relationship('Dks',
                         back_populates='FIELD',
                         cascade="all, delete-orphan", lazy="selectin")    

class Companies(BaseMethods):
    __tablename__ = 'COMPANIES'
    __table_args__ = {'comment':'Таблица недропользователей'}


    id = Column(Integer, primary_key=True)
    name = Column(String)

    field = relationship('Field',
                         back_populates='COMPANIES',
                         cascade="all, delete-orphan", lazy="selectin")

class Dks(BaseMethods):
    __tablename__ = 'DKS'
    __table_args__ = {'comment':'Таблица ДКС'}


    id = Column(Integer, primary_key=True)
    name = Column(String)

    field_id = Column(Integer, ForeignKey('FIELD.id'))

    field = relationship('Field',
                         back_populates='DKS')
    eq_compressor_unit = relationship('EqCompressorUnit', 
                                back_populates='DKS',
                                cascade="all, delete-orphan", lazy="selectin")        


