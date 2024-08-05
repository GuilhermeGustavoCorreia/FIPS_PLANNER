import pandas as pd
import json
import copy

from previsao_trens.packages.DETELHE.CARREGAR_PAGINA import CARREGAR_RELATORIO_DETALHE as criar_relatorio_detalhe



def montar_html_detalhe(dict_relatorio_detalhe, dia_logistico):

    dias_logisticos = ["D", "D+1", "D+2"]

    html_detalhe_header = f"""
        <table>
            <thead>
                <tr>
                    <th class="CELULA_VAZIA" colspan="2" rowspan="3">
                        
                    </th>
                    <th colspan="14" class="TITULO_AZUL">
                        PREVISÃO {dias_logisticos[dia_logistico]}
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
        
    """

    totais_rumo = dict_relatorio_detalhe["RUMO"]["RUMO"]
    
    print(totais_rumo["GRAOS"]["TOTAL_GRAO"][dia_logistico])

    #region RUMO
    rumo_graos = totais_rumo["GRAOS"]["TOTAL_GRAO"][dia_logistico]

    html_rumo_graos = f"""
    <tr>
        <th rowspan=2>RUMO</th> 
        <th>GRÃO</th>  
        <td>{ rumo_graos["SALDOS"]["P1"]        }</td>
        <td>{ rumo_graos["RECEBIMENTOS"]["P1"]  }</td>
        <td>{ rumo_graos["PEDRA"]["P1"]         }</td> 

        <td>{ rumo_graos["SALDOS"]["P2"]        }</td>
        <td>{ rumo_graos["RECEBIMENTOS"]["P2"]  }</td>
        <td>{ rumo_graos["PEDRA"]["P2"]         }</td>

        <td>{ rumo_graos["SALDOS"]["P3"]        }</td>
        <td>{ rumo_graos["RECEBIMENTOS"]["P3"]  }</td>
        <td>{ rumo_graos["PEDRA"]["P3"]         }</td>

        <td>{ rumo_graos["SALDOS"]["P4"]        }</td>
        <td>{ rumo_graos["RECEBIMENTOS"]["P4"]  }</td>
        <td>{ rumo_graos["PEDRA"]["P4"]         }</td>

        <td>{ rumo_graos["TT_OF"]  }</td>
        <td>{ rumo_graos["TT_PD"]  }</td>
    </tr> """
    
    rumo_acucar = totais_rumo["ACUCAR"]["TOTAL_ACUCAR"][dia_logistico]

    html_rumo_acucar = f"""
    <tr> 
        <th>AÇÚCAR</th>  
        <td>{ rumo_acucar["SALDOS"]["P1"]        }</td>
        <td>{ rumo_acucar["RECEBIMENTOS"]["P1"]  }</td>
        <td>{ rumo_acucar["PEDRA"]["P1"]         }</td> 

        <td>{ rumo_acucar["SALDOS"]["P2"]        }</td>
        <td>{ rumo_acucar["RECEBIMENTOS"]["P2"]  }</td>
        <td>{ rumo_acucar["PEDRA"]["P2"]         }</td>

        <td>{ rumo_acucar["SALDOS"]["P3"]        }</td>
        <td>{ rumo_acucar["RECEBIMENTOS"]["P3"]  }</td>
        <td>{ rumo_acucar["PEDRA"]["P3"]         }</td>

        <td>{ rumo_acucar["SALDOS"]["P4"]        }</td>
        <td>{ rumo_acucar["RECEBIMENTOS"]["P4"]  }</td>
        <td>{ rumo_acucar["PEDRA"]["P4"]         }</td>

        <td>{ rumo_acucar["TT_OF"]  }</td>
        <td>{ rumo_acucar["TT_PD"]  }</td>
    </tr> """

    

    html_rumo = html_rumo_graos + html_rumo_acucar
    
    #endregion



    

    html_detalhe = html_detalhe_header + html_rumo + "</table>"


    
    return html_detalhe

def totais_detalhe(dia_logistico):
    
    dias_logisticos = ["D", "D+1", "D+2"]
    dia_logistico = dias_logisticos.index(dia_logistico)

    dict_relatorio_detalhe = criar_relatorio_detalhe()
    
    del dict_relatorio_detalhe["PRINCIPAL"]
 
    html = montar_html_detalhe(dict_relatorio_detalhe, dia_logistico)
    
    return html