from sqlalchemy_schemadisplay import create_schema_graph
from sqlalchemy.engine import create_engine
from app_name.infrastructure.repositories.compressor.database import Base 
import os
from sqlalchemy import inspect

dot_path = 'C:/JOB/Graphviz-12.2.1-win64/bin'

os.environ["PATH"] += os.pathsep + dot_path 

def format_comment(comment):
    if comment:
        return f'<BR/><FONT POINT-SIZE="10" COLOR="gray">{comment}</FONT>'
    return ""

def generate_er_diagram():
    sync_engine = create_engine("sqlite:///test_dks.db")
    
    with sync_engine.connect() as conn:
        
        graph = create_schema_graph(
            engine=sync_engine,
            metadata=Base.metadata,
            show_datatypes=True,            
            show_indexes=True,
            show_column_keys=True,
            # table_options={
            #     "shape": "plaintext",
            #     "fontname": "Helvetica",
            #     "comment": format_comment, 
            # },
            # column_options={
            #     "comment": format_comment, 
            # }
        )
    print(Base.metadata.sorted_tables)
    models = [cls for cls in Base.__subclasses__()]
    for mapper in Base.registry.mappers:
        model = mapper.class_
        table = model.__table__
        # print(table,model)
    comments = {}
    for model in models:
        # print(f'asd {model}')
        if hasattr(model, '__table__'):
            table = model.__table__
            # print(f'asdsad {table}')
            if hasattr(model, '__table_args__'):
                table_args = model.__table_args__
                if isinstance(table_args, dict):
                    comments[table.name] = table_args.get('comment', '')
                elif isinstance(table_args, tuple):
                    for arg in table_args:
                        if isinstance(arg, dict):
                            comments[table.name] = arg.get('comment', '')
    
    # Добавляем комментарии в граф
    for node in graph.get_nodes():
        table_name = node.get_name().strip('"')
        if table_name in comments and comments[table_name]:
            node.set_label(
                f'<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">'
                f'<TR><TD><B>{table_name}</B></TD></TR>'
                f'<TR><TD ALIGN="LEFT"><FONT POINT-SIZE="10">{comments[table_name]}</FONT></TD></TR>'
                '</TABLE>>'
            )

        graph.write_png('er_diagram.png')
        graph.write_svg('er_diagram.svg')
        
if __name__ == '__main__':
    generate_er_diagram()