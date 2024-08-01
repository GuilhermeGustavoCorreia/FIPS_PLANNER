import pandas as pd
import json
import copy

from previsao_trens.packages.DETELHE.CARREGAR_PAGINA import CARREGAR_RELATORIO_DETALHE as criar_relatorio_detalhe



def montar_html_detalhe(dict_relatorio_detalhe, dia_logistico):

    html_detalhe_header = f"""
        <table>
            <thead>
                <tr>
                    <th class="CELULA_VAZIA" colspan="4" rowspan="3">
                        
                    </th>
                    <th colspan="14" class="TITULO_AZUL">
                        PREVISÃO {dia_logistico}
                    </th>
                   
                </tr>
                
                <tr>

                    <th colspan="3">
                        01h-07h
                    </th>
                    <th colspan="3">
                        07h-13h
                    </th>
                    <th colspan="3">
                        13h-19h
                    </th>
                    <th colspan="3">
                        13h-01h
                    </th>

                    <th colspan="2">
                        TT "D"
                    </th>
            
                </tr>
                
                <tr>


                    <th>EX</th>
                    <th>REC</th>
                    <th>PD</th>
                    
                    <th>SD</th>
                    <th>REC</th>
                    <th>PD</th>

                    <th>SD</th>
                    <th>REC</th>
                    <th>PD</th>

                    <th>SD</th>
                    <th>REC</th>
                    <th>PD</th>

                    <th>OF</th>
                    <th>PD</th>

                </tr>
            
            </thead>
        </table>
    """

    totais_rumo = dict_relatorio_detalhe["RUMO"]
    print(totais_rumo)
    
    html_detalhe = html_detalhe_header

    return html_detalhe

def totais_detalhe(dia_logistico):
    

    
    dict_relatorio_detalhe = criar_relatorio_detalhe()
    
    del dict_relatorio_detalhe["PRINCIPAL"]
 
    html = montar_html_detalhe(dict_relatorio_detalhe, dia_logistico)
    
    return html