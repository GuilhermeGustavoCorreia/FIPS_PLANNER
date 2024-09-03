import pandas as pd
import json
import copy

from previsao_trens.packages.DETELHE.CARREGAR_PAGINA import CARREGAR_RELATORIO_DETALHE as criar_relatorio_detalhe



def montar_html_detalhe(dict_relatorio_detalhe, dia_logistico):
    
    PULA_LINHA = "<tr><td class='pula__linha' colspan=16>x</td></tr>"

    dias_logisticos = ["D", "D+1", "D+2"]
    titulos= ["TITULO_AZUL", "TITULO_VERDE", "TITULO_AZUL"]
    html_detalhe_header = f"""
        <table id="relatorio_detalhe">
            <thead>
                <tr>
                    <th class="CELULA_VAZIA"  rowspan="3">
                        
                    </th>
                    <th colspan="14" class="{titulos[dia_logistico]}">
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
                        TT "{dias_logisticos[dia_logistico]}"
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
    
    #region MRS
  
    mrs_graos_psn = dict_relatorio_detalhe["MRS"]["GRAOS"]['PSN'][dia_logistico]
    html_mrs_graos_psn = ""
    if (int(mrs_graos_psn["TT_OF"]) + int(mrs_graos_psn["TT_PD"])) > 0:
        html_mrs_graos_psn = f"""
        <tr>
            <th class="NOME__TERMINAL">MRS GRÃOS PSN</th> 
            
            <td class="CONTEUDO_{dia_logistico}">{ mrs_graos_psn["SALDOS"]["P1"]}</td>
            <td class="CONTEUDO_{dia_logistico}">{ mrs_graos_psn["RECEBIMENTOS"]["P1"]}</td> 
            <td class="CONTEUDO_PD{dia_logistico}">{ mrs_graos_psn["PEDRA"]["P1"]}</td>  

            <td class="CONTEUDO_{dia_logistico}">{ mrs_graos_psn["SALDOS"]["P2"]}</td>
            <td class="CONTEUDO_{dia_logistico}">{ mrs_graos_psn["RECEBIMENTOS"]["P2"]}</td>
            <td class="CONTEUDO_PD{dia_logistico}">{ mrs_graos_psn["PEDRA"]["P2"]}</td>

            <td class="CONTEUDO_{dia_logistico}">{ mrs_graos_psn["SALDOS"]["P3"]}</td>
            <td class="CONTEUDO_{dia_logistico}">{ mrs_graos_psn["RECEBIMENTOS"]["P3"]}</td>
            <td class="CONTEUDO_PD{dia_logistico}">{ mrs_graos_psn["PEDRA"]["P3"]}</td>

            <td class="CONTEUDO_{dia_logistico}">{ mrs_graos_psn["SALDOS"]["P4"]}</td>
            <td class="CONTEUDO_{dia_logistico}">{ mrs_graos_psn["RECEBIMENTOS"]["P4"]}</td>
            <td class="CONTEUDO_PD{dia_logistico}"> { mrs_graos_psn["PEDRA"]["P4"]}</td>

            <td class="COLUNA_TOTAL">{ mrs_graos_psn["TT_OF"]}</td> 
            <td class="COLUNA_TOTAL">{ mrs_graos_psn["TT_PD"]}</td>
        </tr> """

    mrs_graos_pcz = dict_relatorio_detalhe["MRS"]["GRAOS"]['PCZ'][dia_logistico]
    html_mrs_graos_pcz = "" 
    if (int(mrs_graos_pcz["TT_OF"]) + int(mrs_graos_pcz["TT_PD"])) > 0:   
        html_mrs_graos_pcz = f"""
        <tr>
            <th class="NOME__TERMINAL">MRS GRÃOS PCZ</th> 
            
            <td class="CONTEUDO_{dia_logistico}">{ mrs_graos_pcz["SALDOS"]["P1"]           }</td>
            <td class="CONTEUDO_{dia_logistico}">{ mrs_graos_pcz["RECEBIMENTOS"]["P1"]     }</td> 
            <td class="CONTEUDO_PD{dia_logistico}">{ mrs_graos_pcz["PEDRA"]["P1"]            }</td>  

            <td class="CONTEUDO_{dia_logistico}">{ mrs_graos_pcz["SALDOS"]["P2"]           }</td>
            <td class="CONTEUDO_{dia_logistico}">{ mrs_graos_pcz["RECEBIMENTOS"]["P2"]     }</td>
            <td class="CONTEUDO_PD{dia_logistico}">{ mrs_graos_pcz["PEDRA"]["P2"]            }</td>

            <td class="CONTEUDO_{dia_logistico}">{ mrs_graos_pcz["SALDOS"]["P3"]           }</td>
            <td class="CONTEUDO_{dia_logistico}">{ mrs_graos_pcz["RECEBIMENTOS"]["P3"]     }</td>
            <td class="CONTEUDO_PD{dia_logistico}">{ mrs_graos_pcz["PEDRA"]["P3"]            }</td>

            <td class="CONTEUDO_{dia_logistico}">{ mrs_graos_pcz["SALDOS"]["P4"]           }</td>
            <td class="CONTEUDO_{dia_logistico}">{ mrs_graos_pcz["RECEBIMENTOS"]["P4"]     }</td>
            <td class="CONTEUDO_PD{dia_logistico}">{ mrs_graos_pcz["PEDRA"]["P4"]            }</td>

            <td class="COLUNA_TOTAL">{ mrs_graos_pcz["TT_OF"]  }</td> 
            <td class="COLUNA_TOTAL">{ mrs_graos_pcz["TT_PD"]  }</td>
        </tr> """

    mrs_acucar_psn = dict_relatorio_detalhe["MRS"]["ACUCAR"]['PSN'][dia_logistico]
    html_mrs_acucar_psn = ""
    if (int(mrs_acucar_psn["TT_OF"]) + int(mrs_acucar_psn["TT_PD"])) > 0: 
        html_mrs_acucar_psn = f"""
        <tr>
            <th class="NOME__TERMINAL">MRS AÇÚCAR PSN</th> 
            
            <td class="CONTEUDO_{dia_logistico}">{ mrs_acucar_psn["SALDOS"]["P1"]           }</td>
            <td class="CONTEUDO_{dia_logistico}">{ mrs_acucar_psn["RECEBIMENTOS"]["P1"]     }</td> 
            <td class="CONTEUDO_PD{dia_logistico}">{ mrs_acucar_psn["PEDRA"]["P1"]            }</td>  

            <td class="CONTEUDO_{dia_logistico}">{ mrs_acucar_psn["SALDOS"]["P2"]           }</td>
            <td class="CONTEUDO_{dia_logistico}">{ mrs_acucar_psn["RECEBIMENTOS"]["P2"]     }</td>
            <td class="CONTEUDO_PD{dia_logistico}">{ mrs_acucar_psn["PEDRA"]["P2"]            }</td>

            <td class="CONTEUDO_{dia_logistico}">{ mrs_acucar_psn["SALDOS"]["P3"]           }</td>
            <td class="CONTEUDO_{dia_logistico}">{ mrs_acucar_psn["RECEBIMENTOS"]["P3"]     }</td>
            <td class="CONTEUDO_PD{dia_logistico}">{ mrs_acucar_psn["PEDRA"]["P3"]            }</td>

            <td class="CONTEUDO_{dia_logistico}">{ mrs_acucar_psn["SALDOS"]["P4"]           }</td>
            <td class="CONTEUDO_{dia_logistico}">{ mrs_acucar_psn["RECEBIMENTOS"]["P4"]     }</td>
            <td class="CONTEUDO_PD{dia_logistico}">{ mrs_acucar_psn["PEDRA"]["P4"]            }</td>

            <td class="COLUNA_TOTAL">{ mrs_acucar_psn["TT_OF"]  }</td> 
            <td class="COLUNA_TOTAL">{ mrs_acucar_psn["TT_PD"]  }</td>
        </tr> """

    mrs_acucar_pcz = dict_relatorio_detalhe["MRS"]["ACUCAR"]['PCZ'][dia_logistico]
    html_mrs_acucar_pcz = ""
    if (int(mrs_acucar_pcz["TT_OF"]) + int(mrs_acucar_pcz["TT_PD"])) > 0:
        html_mrs_acucar_pcz = f"""
        <tr>
            <th class="NOME__TERMINAL">MRS AÇÚCAR PCZ</th> 
            
            <td class="CONTEUDO_{dia_logistico}">   { mrs_acucar_pcz["SALDOS"]["P1"]           }</td>
            <td class="CONTEUDO_{dia_logistico}">   { mrs_acucar_pcz["RECEBIMENTOS"]["P1"]     }</td> 
            <td class="CONTEUDO_PD{dia_logistico}"> { mrs_acucar_pcz["PEDRA"]["P1"]            }</td>  

            <td class="CONTEUDO_{dia_logistico}">   { mrs_acucar_pcz["SALDOS"]["P2"]           }</td>
            <td class="CONTEUDO_{dia_logistico}">   { mrs_acucar_pcz["RECEBIMENTOS"]["P2"]     }</td>
            <td class="CONTEUDO_PD{dia_logistico}"> { mrs_acucar_pcz["PEDRA"]["P2"]            }</td>

            <td class="CONTEUDO_{dia_logistico}">   { mrs_acucar_pcz["SALDOS"]["P3"]           }</td>
            <td class="CONTEUDO_{dia_logistico}">   { mrs_acucar_pcz["RECEBIMENTOS"]["P3"]     }</td>
            <td class="CONTEUDO_PD{dia_logistico}"> { mrs_acucar_pcz["PEDRA"]["P3"]            }</td>

            <td class="CONTEUDO_{dia_logistico}">   { mrs_acucar_pcz["SALDOS"]["P4"]           }</td>
            <td class="CONTEUDO_{dia_logistico}">   { mrs_acucar_pcz["RECEBIMENTOS"]["P4"]     }</td>
            <td class="CONTEUDO_PD{dia_logistico}"> { mrs_acucar_pcz["PEDRA"]["P4"]            }</td>

            <td class="COLUNA_TOTAL">{ mrs_acucar_pcz["TT_OF"]  }</td> 
            <td class="COLUNA_TOTAL">{ mrs_acucar_pcz["TT_PD"]  }</td>
        </tr> """

    mrs_graos_e_acucar = dict_relatorio_detalhe["MRS"]["TOTAO_GRAO_ACUCAR"][dia_logistico] 
    html_total_mrs_graos_e_acucar = ""
    if (int(mrs_graos_e_acucar["TT_OF"]) + int(mrs_graos_e_acucar["TT_PD"])) > 0:
        html_total_mrs_graos_e_acucar = f"""
        <tr>
            <th class="COLUNA_TOTAL NOME__TERMINAL">TOTAL MRS GRÃOS E AÇÚCAR</th> 
            
            <td class="TOTAL_{dia_logistico}">      { mrs_graos_e_acucar["SALDOS"]["P1"]        }</td>
            <td class="TOTAL_{dia_logistico}">      { mrs_graos_e_acucar["RECEBIMENTOS"]["P1"]  }</td>
            <td class="TOTAL_PD{dia_logistico}">    { mrs_graos_e_acucar["PEDRA"]["P1"]         }</td> 

            <td class="TOTAL_{dia_logistico}">      { mrs_graos_e_acucar["SALDOS"]["P2"]        }</td>
            <td class="TOTAL_{dia_logistico}">      { mrs_graos_e_acucar["RECEBIMENTOS"]["P2"]  }</td>
            <td class="TOTAL_PD{dia_logistico}">    { mrs_graos_e_acucar["PEDRA"]["P2"]         }</td>

            <td class="TOTAL_{dia_logistico}">      { mrs_graos_e_acucar["SALDOS"]["P3"]        }</td>
            <td class="TOTAL_{dia_logistico}">      { mrs_graos_e_acucar["RECEBIMENTOS"]["P3"]  }</td>
            <td class="TOTAL_PD{dia_logistico}">    { mrs_graos_e_acucar["PEDRA"]["P3"]         }</td>

            <td class="TOTAL_{dia_logistico}">      { mrs_graos_e_acucar["SALDOS"]["P4"]        }</td>
            <td class="TOTAL_{dia_logistico}">      { mrs_graos_e_acucar["RECEBIMENTOS"]["P4"]  }</td>
            <td class="TOTAL_PD{dia_logistico}">    { mrs_graos_e_acucar["PEDRA"]["P4"]         }</td>

            <td class="TOTAL_TOTAL{dia_logistico}"> { mrs_graos_e_acucar["TT_OF"]  }</td>
            <td class="TOTAL_TOTAL{dia_logistico}"> { mrs_graos_e_acucar["TT_PD"]  }</td>
        </tr> """

    mrs_celulose_psn = dict_relatorio_detalhe["MRS"]["CELULOSE"]["PSN"][dia_logistico] 
    html_mrs_celulose_psn = ""
    if (int(mrs_celulose_psn["TT_OF"]) + int(mrs_celulose_psn["TT_PD"])) > 0:
        html_mrs_celulose_psn = f"""
        <tr>
            <th class="NOME__TERMINAL">MRS CELULOSE PSN</th> 
            
            <td class="CONTEUDO_{dia_logistico}">   { mrs_celulose_psn["SALDOS"]["P1"]           }</td>
            <td class="CONTEUDO_{dia_logistico}">   { mrs_celulose_psn["RECEBIMENTOS"]["P1"]     }</td> 
            <td class="CONTEUDO_PD{dia_logistico}"> { mrs_celulose_psn["PEDRA"]["P1"]            }</td>  

            <td class="CONTEUDO_{dia_logistico}">   { mrs_celulose_psn["SALDOS"]["P2"]           }</td>
            <td class="CONTEUDO_{dia_logistico}">   { mrs_celulose_psn["RECEBIMENTOS"]["P2"]     }</td>
            <td class="CONTEUDO_PD{dia_logistico}"> { mrs_celulose_psn["PEDRA"]["P2"]            }</td>

            <td class="CONTEUDO_{dia_logistico}">   { mrs_celulose_psn["SALDOS"]["P3"]           }</td>
            <td class="CONTEUDO_{dia_logistico}">   { mrs_celulose_psn["RECEBIMENTOS"]["P3"]     }</td>
            <td class="CONTEUDO_PD{dia_logistico}"> { mrs_celulose_psn["PEDRA"]["P3"]            }</td>

            <td class="CONTEUDO_{dia_logistico}">   { mrs_celulose_psn["SALDOS"]["P4"]           }</td>
            <td class="CONTEUDO_{dia_logistico}">   { mrs_celulose_psn["RECEBIMENTOS"]["P4"]     }</td>
            <td class="CONTEUDO_PD{dia_logistico}"> { mrs_celulose_psn["PEDRA"]["P4"]            }</td>

            <td class="COLUNA_TOTAL">{ mrs_celulose_psn["TT_OF"]  }</td> 
            <td class="COLUNA_TOTAL">{ mrs_celulose_psn["TT_PD"]  }</td>
        </tr> """

    total_mrs_celulose = dict_relatorio_detalhe["MRS"]["CELULOSE"]["TOTAL_CELULOSE"][dia_logistico] 
    html_total_total_mrs_celulose = ""
    if (int(total_mrs_celulose["TT_OF"]) + int(total_mrs_celulose["TT_PD"])) > 0:
        html_total_total_mrs_celulose = f"""
        <tr>
            <th class="COLUNA_TOTAL NOME__TERMINAL">TOTAL MRS CELULOSE</th> 
            
            <td class="TOTAL_{dia_logistico}">      { total_mrs_celulose["SALDOS"]["P1"]        }</td>
            <td class="TOTAL_{dia_logistico}">      { total_mrs_celulose["RECEBIMENTOS"]["P1"]  }</td>
            <td class="TOTAL_PD{dia_logistico}">    { total_mrs_celulose["PEDRA"]["P1"]         }</td> 

            <td class="TOTAL_{dia_logistico}">      { total_mrs_celulose["SALDOS"]["P2"]        }</td>
            <td class="TOTAL_{dia_logistico}">      { total_mrs_celulose["RECEBIMENTOS"]["P2"]  }</td>
            <td class="TOTAL_PD{dia_logistico}">    { total_mrs_celulose["PEDRA"]["P2"]         }</td>

            <td class="TOTAL_{dia_logistico}">      { total_mrs_celulose["SALDOS"]["P3"]        }</td>
            <td class="TOTAL_{dia_logistico}">      { total_mrs_celulose["RECEBIMENTOS"]["P3"]  }</td>
            <td class="TOTAL_PD{dia_logistico}">    { total_mrs_celulose["PEDRA"]["P3"]         }</td>

            <td class="TOTAL_{dia_logistico}">      { total_mrs_celulose["SALDOS"]["P4"]        }</td>
            <td class="TOTAL_{dia_logistico}">      { total_mrs_celulose["RECEBIMENTOS"]["P4"]  }</td>
            <td class="TOTAL_PD{dia_logistico}">    { total_mrs_celulose["PEDRA"]["P4"]         }</td>

            <td class="TOTAL_TOTAL{dia_logistico}"> { total_mrs_celulose["TT_OF"]  }</td>
            <td class="TOTAL_TOTAL{dia_logistico}"> { total_mrs_celulose["TT_PD"]  }</td>
        </tr> """

    mrs_conteiner_psn = dict_relatorio_detalhe["MRS"]["CONTEINER"]["PSN"][dia_logistico] 
    html_mrs_conteiner_psn = ""
    if (int(mrs_conteiner_psn["TT_OF"]) + int(mrs_conteiner_psn["TT_PD"])) > 0:
        html_mrs_conteiner_psn = f"""
        <tr>
            <th class="NOME__TERMINAL">MRS CONTEINER PSN</th> 
            
            <td class="CONTEUDO_{dia_logistico}">   { mrs_conteiner_psn["SALDOS"]["P1"]           }</td>
            <td class="CONTEUDO_{dia_logistico}">   { mrs_conteiner_psn["RECEBIMENTOS"]["P1"]     }</td> 
            <td class="CONTEUDO_PD{dia_logistico}"> { mrs_conteiner_psn["PEDRA"]["P1"]            }</td>  

            <td class="CONTEUDO_{dia_logistico}">   { mrs_conteiner_psn["SALDOS"]["P2"]           }</td>
            <td class="CONTEUDO_{dia_logistico}">   { mrs_conteiner_psn["RECEBIMENTOS"]["P2"]     }</td>
            <td class="CONTEUDO_PD{dia_logistico}"> { mrs_conteiner_psn["PEDRA"]["P2"]            }</td>

            <td class="CONTEUDO_{dia_logistico}">   { mrs_conteiner_psn["SALDOS"]["P3"]           }</td>
            <td class="CONTEUDO_{dia_logistico}">   { mrs_conteiner_psn["RECEBIMENTOS"]["P3"]     }</td>
            <td class="CONTEUDO_PD{dia_logistico}"> { mrs_conteiner_psn["PEDRA"]["P3"]            }</td>

            <td class="CONTEUDO_{dia_logistico}">   { mrs_conteiner_psn["SALDOS"]["P4"]           }</td>
            <td class="CONTEUDO_{dia_logistico}">   { mrs_conteiner_psn["RECEBIMENTOS"]["P4"]     }</td>
            <td class="CONTEUDO_PD{dia_logistico}"> { mrs_conteiner_psn["PEDRA"]["P4"]            }</td>

            <td class="COLUNA_TOTAL">{ mrs_conteiner_psn["TT_OF"]  }</td> 
            <td class="COLUNA_TOTAL">{ mrs_conteiner_psn["TT_PD"]  }</td>

        </tr> """

    mrs_conteiner_pcz = dict_relatorio_detalhe["MRS"]["CONTEINER"]["PCZ"][dia_logistico] 
    html_mrs_conteiner_pcz = ""
    if (int(mrs_conteiner_pcz["TT_OF"]) + int(mrs_conteiner_pcz["TT_PD"])) > 0:
        html_mrs_conteiner_pcz = f"""
        <tr>
            <th class="NOME__TERMINAL">MRS CONTEINER PCZ</th> 
            
            <td class="CONTEUDO_{dia_logistico}">   { mrs_conteiner_pcz["SALDOS"]["P1"]           }</td>
            <td class="CONTEUDO_{dia_logistico}">   { mrs_conteiner_pcz["RECEBIMENTOS"]["P1"]     }</td> 
            <td class="CONTEUDO_PD{dia_logistico}"> { mrs_conteiner_pcz["PEDRA"]["P1"]            }</td>  

            <td class="CONTEUDO_{dia_logistico}">   { mrs_conteiner_pcz["SALDOS"]["P2"]           }</td>
            <td class="CONTEUDO_{dia_logistico}">   { mrs_conteiner_pcz["RECEBIMENTOS"]["P2"]     }</td>
            <td class="CONTEUDO_PD{dia_logistico}"> { mrs_conteiner_pcz["PEDRA"]["P2"]            }</td>

            <td class="CONTEUDO_{dia_logistico}">   { mrs_conteiner_pcz["SALDOS"]["P3"]           }</td>
            <td class="CONTEUDO_{dia_logistico}">   { mrs_conteiner_pcz["RECEBIMENTOS"]["P3"]     }</td>
            <td class="CONTEUDO_PD{dia_logistico}"> { mrs_conteiner_pcz["PEDRA"]["P3"]            }</td>

            <td class="CONTEUDO_{dia_logistico}">   { mrs_conteiner_pcz["SALDOS"]["P4"]           }</td>
            <td class="CONTEUDO_{dia_logistico}">   { mrs_conteiner_pcz["RECEBIMENTOS"]["P4"]     }</td>
            <td class="CONTEUDO_PD{dia_logistico}"> { mrs_conteiner_pcz["PEDRA"]["P4"]            }</td>

            <td class="COLUNA_TOTAL">{ mrs_conteiner_pcz["TT_OF"]  }</td> 
            <td class="COLUNA_TOTAL">{ mrs_conteiner_pcz["TT_PD"]  }</td>
        </tr> """

    total_mrs_conteiner = dict_relatorio_detalhe["MRS"]["CONTEINER"]["TOTAL_CONTEINER"][dia_logistico] 
    html_total_total_mrs_conteiner = ""
    if (int(total_mrs_conteiner["TT_OF"]) + int(total_mrs_conteiner["TT_PD"])) > 0:
        html_total_total_mrs_conteiner = f"""
        <tr>
            <th class="COLUNA_TOTAL NOME__TERMINAL">TOTAL MRS CONTEINER</th> 
            
            <td class="TOTAL_{dia_logistico}">      { total_mrs_conteiner["SALDOS"]["P1"]        }</td>
            <td class="TOTAL_{dia_logistico}">      { total_mrs_conteiner["RECEBIMENTOS"]["P1"]  }</td>
            <td class="TOTAL_PD{dia_logistico}">    { total_mrs_conteiner["PEDRA"]["P1"]         }</td> 

            <td class="TOTAL_{dia_logistico}">      { total_mrs_conteiner["SALDOS"]["P2"]        }</td>
            <td class="TOTAL_{dia_logistico}">      { total_mrs_conteiner["RECEBIMENTOS"]["P2"]  }</td>
            <td class="TOTAL_PD{dia_logistico}">    { total_mrs_conteiner["PEDRA"]["P2"]         }</td>

            <td class="TOTAL_{dia_logistico}">      { total_mrs_conteiner["SALDOS"]["P3"]        }</td>
            <td class="TOTAL_{dia_logistico}">      { total_mrs_conteiner["RECEBIMENTOS"]["P3"]  }</td>
            <td class="TOTAL_PD{dia_logistico}">    { total_mrs_conteiner["PEDRA"]["P3"]         }</td>

            <td class="TOTAL_{dia_logistico}">      { total_mrs_conteiner["SALDOS"]["P4"]        }</td>
            <td class="TOTAL_{dia_logistico}">      { total_mrs_conteiner["RECEBIMENTOS"]["P4"]  }</td>
            <td class="TOTAL_PD{dia_logistico}">    { total_mrs_conteiner["PEDRA"]["P4"]         }</td>

            <td class="TOTAL_TOTAL{dia_logistico}"> { total_mrs_conteiner["TT_OF"]  }</td>
            <td class="TOTAL_TOTAL{dia_logistico}"> { total_mrs_conteiner["TT_PD"]  }</td>
        </tr> """

    html_mrs = ( 
        html_mrs_graos_psn  + 
        html_mrs_graos_pcz  +
        html_mrs_acucar_psn +
        html_mrs_acucar_pcz +
        html_total_mrs_graos_e_acucar +
        html_mrs_celulose_psn +
        html_total_total_mrs_celulose +
        html_mrs_conteiner_psn +
        html_mrs_conteiner_pcz +
        html_total_total_mrs_conteiner 
        )

    #endregion

    #region RUMO
    
    rumo_graos_e_acucar = dict_relatorio_detalhe["RUMO"]["TOTAIS"]["GRAO_ACUCAR"][dia_logistico] 
    html_total_rumo_graos_e_acucar =  ""
    if (int(rumo_graos_e_acucar["TT_OF"]) + int(rumo_graos_e_acucar["TT_PD"])) > 0:
        html_total_rumo_graos_e_acucar = f"""
        <tr>
            <th class="COLUNA_TOTAL NOME__TERMINAL">TOTAL RUMO GRÃOS E AÇÚCAR</th> 
            
            <td class="TOTAL_{dia_logistico}">      { rumo_graos_e_acucar["SALDOS"]["P1"]        }</td>
            <td class="TOTAL_{dia_logistico}">      { rumo_graos_e_acucar["RECEBIMENTOS"]["P1"]  }</td>
            <td class="TOTAL_PD{dia_logistico}">    { rumo_graos_e_acucar["PEDRA"]["P1"]         }</td> 

            <td class="TOTAL_{dia_logistico}">      { rumo_graos_e_acucar["SALDOS"]["P2"]        }</td>
            <td class="TOTAL_{dia_logistico}">      { rumo_graos_e_acucar["RECEBIMENTOS"]["P2"]  }</td>
            <td class="TOTAL_PD{dia_logistico}">    { rumo_graos_e_acucar["PEDRA"]["P2"]         }</td>

            <td class="TOTAL_{dia_logistico}">      { rumo_graos_e_acucar["SALDOS"]["P3"]        }</td>
            <td class="TOTAL_{dia_logistico}">      { rumo_graos_e_acucar["RECEBIMENTOS"]["P3"]  }</td>
            <td class="TOTAL_PD{dia_logistico}">    { rumo_graos_e_acucar["PEDRA"]["P3"]         }</td>

            <td class="TOTAL_{dia_logistico}">      { rumo_graos_e_acucar["SALDOS"]["P4"]        }</td>
            <td class="TOTAL_{dia_logistico}">      { rumo_graos_e_acucar["RECEBIMENTOS"]["P4"]  }</td>
            <td class="TOTAL_PD{dia_logistico}">    { rumo_graos_e_acucar["PEDRA"]["P4"]         }</td>

            <td class="TOTAL_TOTAL{dia_logistico}"> { rumo_graos_e_acucar["TT_OF"]  }</td>
            <td class="TOTAL_TOTAL{dia_logistico}"> { rumo_graos_e_acucar["TT_PD"]  }</td>
        </tr> """

    rumo_graos_psn = dict_relatorio_detalhe["RUMO"]["RUMO"]["GRAOS"]['PSN'][dia_logistico]
    html_rumo_graos_psn = ""
    if (int(rumo_graos_psn["TT_OF"]) + int(rumo_graos_psn["TT_PD"])) > 0:
        html_rumo_graos_psn = f"""
        <tr>
            <th class="NOME__TERMINAL">RUMO GRÃOS PSN</th> 
            
            <td class="CONTEUDO_{dia_logistico}">   { rumo_graos_psn["SALDOS"]["P1"]           }</td>
            <td class="CONTEUDO_{dia_logistico}">   { rumo_graos_psn["RECEBIMENTOS"]["P1"]     }</td> 
            <td class="CONTEUDO_PD{dia_logistico}"> { rumo_graos_psn["PEDRA"]["P1"]            }</td>  

            <td class="CONTEUDO_{dia_logistico}">   { rumo_graos_psn["SALDOS"]["P2"]           }</td>
            <td class="CONTEUDO_{dia_logistico}">   { rumo_graos_psn["RECEBIMENTOS"]["P2"]     }</td>
            <td class="CONTEUDO_PD{dia_logistico}"> { rumo_graos_psn["PEDRA"]["P2"]            }</td>

            <td class="CONTEUDO_{dia_logistico}">   { rumo_graos_psn["SALDOS"]["P3"]           }</td>
            <td class="CONTEUDO_{dia_logistico}">   { rumo_graos_psn["RECEBIMENTOS"]["P3"]     }</td>
            <td class="CONTEUDO_PD{dia_logistico}"> { rumo_graos_psn["PEDRA"]["P3"]            }</td>

            <td class="CONTEUDO_{dia_logistico}">   { rumo_graos_psn["SALDOS"]["P4"]           }</td>
            <td class="CONTEUDO_{dia_logistico}">   { rumo_graos_psn["RECEBIMENTOS"]["P4"]     }</td>
            <td class="CONTEUDO_PD{dia_logistico}"> { rumo_graos_psn["PEDRA"]["P4"]            }</td>

            <td class="COLUNA_TOTAL">{ rumo_graos_psn["TT_OF"]  }</td> 
            <td class="COLUNA_TOTAL">{ rumo_graos_psn["TT_PD"]  }</td>
        </tr> """

    rumo_graos_pcz = dict_relatorio_detalhe["RUMO"]["RUMO"]["GRAOS"]['PCZ'][dia_logistico]
    html_rumo_graos_pcz = ""
    if (int(rumo_graos_pcz["TT_OF"]) + int(rumo_graos_pcz["TT_PD"])) > 0:
        html_rumo_graos_pcz = f"""
        <tr>
            <th class="NOME__TERMINAL">RUMO GRÃOS PCZ</th> 
            
            <td class="CONTEUDO_{dia_logistico}">   { rumo_graos_pcz["SALDOS"]["P1"]        }</td>
            <td class="CONTEUDO_{dia_logistico}">   { rumo_graos_pcz["RECEBIMENTOS"]["P1"]  }</td>
            <td class="CONTEUDO_PD{dia_logistico}"> { rumo_graos_pcz["PEDRA"]["P1"]         }</td> 

            <td class="CONTEUDO_{dia_logistico}">   { rumo_graos_pcz["SALDOS"]["P2"]        }</td>
            <td class="CONTEUDO_{dia_logistico}">   { rumo_graos_pcz["RECEBIMENTOS"]["P2"]  }</td>
            <td class="CONTEUDO_PD{dia_logistico}"> { rumo_graos_pcz["PEDRA"]["P2"]         }</td>

            <td class="CONTEUDO_{dia_logistico}">   { rumo_graos_pcz["SALDOS"]["P3"]        }</td>
            <td class="CONTEUDO_{dia_logistico}">   { rumo_graos_pcz["RECEBIMENTOS"]["P3"]  }</td>
            <td class="CONTEUDO_PD{dia_logistico}"> { rumo_graos_pcz["PEDRA"]["P3"]         }</td>

            <td class="CONTEUDO_{dia_logistico}">   { rumo_graos_pcz["SALDOS"]["P4"]        }</td>
            <td class="CONTEUDO_{dia_logistico}">   { rumo_graos_pcz["RECEBIMENTOS"]["P4"]  }</td>
            <td class="CONTEUDO_PD{dia_logistico}"> { rumo_graos_pcz["PEDRA"]["P4"]         }</td>

            <td class="COLUNA_TOTAL">{ rumo_graos_pcz["TT_OF"]  }</td>
            <td class="COLUNA_TOTAL">{ rumo_graos_pcz["TT_PD"]  }</td>
        </tr> """
    
    rumo_graos = totais_rumo["GRAOS"]["TOTAL_GRAO"][dia_logistico]
    html_total_rumo_graos = ""
    if (int(rumo_graos["TT_OF"]) + int(rumo_graos["TT_PD"])) > 0:
        html_total_rumo_graos = f"""
        <tr>

            <th class="COLUNA_TOTAL NOME__TERMINAL">TOTAL RUMO GRÃOS</th>  
            <td class="TOTAL_{dia_logistico}">      { rumo_graos["SALDOS"]["P1"]        }</td>
            <td class="TOTAL_{dia_logistico}">      { rumo_graos["RECEBIMENTOS"]["P1"]  }</td>
            <td class="TOTAL_PD{dia_logistico}">    { rumo_graos["PEDRA"]["P1"]         }</td> 

            <td class="TOTAL_{dia_logistico}">      { rumo_graos["SALDOS"]["P2"]        }</td>
            <td class="TOTAL_{dia_logistico}">      { rumo_graos["RECEBIMENTOS"]["P2"]  }</td>
            <td class="TOTAL_PD{dia_logistico}">    { rumo_graos["PEDRA"]["P2"]         }</td>

            <td class="TOTAL_{dia_logistico}">      { rumo_graos["SALDOS"]["P3"]        }</td>
            <td class="TOTAL_{dia_logistico}">      { rumo_graos["RECEBIMENTOS"]["P3"]  }</td>
            <td class="TOTAL_PD{dia_logistico}">    { rumo_graos["PEDRA"]["P3"]         }</td>

            <td class="TOTAL_{dia_logistico}">      { rumo_graos["SALDOS"]["P4"]        }</td>
            <td class="TOTAL_{dia_logistico}">      { rumo_graos["RECEBIMENTOS"]["P4"]  }</td>
            <td class="TOTAL_PD{dia_logistico}">    { rumo_graos["PEDRA"]["P4"]         }</td>

            <td class="TOTAL_TOTAL{dia_logistico}"> { rumo_graos["TT_OF"]  }</td>
            <td class="TOTAL_TOTAL{dia_logistico}"> { rumo_graos["TT_PD"]  }</td>
        </tr> """
    
    rumo_acucar_psn = dict_relatorio_detalhe["RUMO"]["RUMO"]["ACUCAR"]['PSN'][dia_logistico]
    html_rumo_acucar_psn = ""
    if (int(rumo_acucar_psn["TT_OF"]) + int(rumo_acucar_psn["TT_PD"])) > 0:
        html_rumo_acucar_psn = f"""
        <tr>
            <th class="NOME__TERMINAL">RUMO AÇÚCAR PSN</th> 
            
            <td class="CONTEUDO_{dia_logistico}">   { rumo_acucar_psn["SALDOS"]["P1"]        }</td>
            <td class="CONTEUDO_{dia_logistico}">   { rumo_acucar_psn["RECEBIMENTOS"]["P1"]  }</td>
            <td class="CONTEUDO_PD{dia_logistico}"> { rumo_acucar_psn["PEDRA"]["P1"]         }</td> 

            <td class="CONTEUDO_{dia_logistico}">   { rumo_acucar_psn["SALDOS"]["P2"]        }</td>
            <td class="CONTEUDO_{dia_logistico}">   { rumo_acucar_psn["RECEBIMENTOS"]["P2"]  }</td>
            <td class="CONTEUDO_PD{dia_logistico}"> { rumo_acucar_psn["PEDRA"]["P2"]         }</td>

            <td class="CONTEUDO_{dia_logistico}">   { rumo_acucar_psn["SALDOS"]["P3"]        }</td>
            <td class="CONTEUDO_{dia_logistico}">   { rumo_acucar_psn["RECEBIMENTOS"]["P3"]  }</td>
            <td class="CONTEUDO_PD{dia_logistico}"> { rumo_acucar_psn["PEDRA"]["P3"]         }</td>

            <td class="CONTEUDO_{dia_logistico}">   { rumo_acucar_psn["SALDOS"]["P4"]        }</td>
            <td class="CONTEUDO_{dia_logistico}">   { rumo_acucar_psn["RECEBIMENTOS"]["P4"]  }</td>
            <td class="CONTEUDO_PD{dia_logistico}"> { rumo_acucar_psn["PEDRA"]["P4"]         }</td>

            <td class="COLUNA_TOTAL">{ rumo_acucar_psn["TT_OF"]  }</td>
            <td class="COLUNA_TOTAL">{ rumo_acucar_psn["TT_PD"]  }</td>
        </tr> """

    rumo_acucar_pcz = dict_relatorio_detalhe["RUMO"]["RUMO"]["ACUCAR"]['PCZ'][dia_logistico]
    html_rumo_acucar_pcz = ""
    if (int(rumo_acucar_pcz["TT_OF"]) + int(rumo_acucar_pcz["TT_PD"])) > 0:
        html_rumo_acucar_pcz = f"""
        <tr>
            <th class="NOME__TERMINAL">RUMO AÇÚCAR PCZ</th> 
            
            <td class="CONTEUDO_{dia_logistico}">   { rumo_acucar_pcz["SALDOS"]["P1"]        }</td>
            <td class="CONTEUDO_{dia_logistico}">   { rumo_acucar_pcz["RECEBIMENTOS"]["P1"]  }</td>
            <td class="CONTEUDO_PD{dia_logistico}"> { rumo_acucar_pcz["PEDRA"]["P1"]         }</td> 

            <td class="CONTEUDO_{dia_logistico}">   { rumo_acucar_pcz["SALDOS"]["P2"]        }</td>
            <td class="CONTEUDO_{dia_logistico}">   { rumo_acucar_pcz["RECEBIMENTOS"]["P2"]  }</td>
            <td class="CONTEUDO_PD{dia_logistico}"> { rumo_acucar_pcz["PEDRA"]["P2"]         }</td>

            <td class="CONTEUDO_{dia_logistico}">   { rumo_acucar_pcz["SALDOS"]["P3"]        }</td>
            <td class="CONTEUDO_{dia_logistico}">   { rumo_acucar_pcz["RECEBIMENTOS"]["P3"]  }</td>
            <td class="CONTEUDO_PD{dia_logistico}"> { rumo_acucar_pcz["PEDRA"]["P3"]         }</td>

            <td class="CONTEUDO_{dia_logistico}">   { rumo_acucar_pcz["SALDOS"]["P4"]        }</td>
            <td class="CONTEUDO_{dia_logistico}">   { rumo_acucar_pcz["RECEBIMENTOS"]["P4"]  }</td>
            <td class="CONTEUDO_PD{dia_logistico}"> { rumo_acucar_pcz["PEDRA"]["P4"]         }</td>

            <td class="COLUNA_TOTAL">{ rumo_acucar_pcz["TT_OF"]  }</td>
            <td class="COLUNA_TOTAL">{ rumo_acucar_pcz["TT_PD"]  }</td>
        </tr> """
    
    rumo_acucar = totais_rumo["ACUCAR"]["TOTAL_ACUCAR"][dia_logistico]
    html_total_rumo_acucar = ""
    if (int(rumo_acucar["TT_OF"]) + int(rumo_acucar["TT_PD"])) > 0:
        html_total_rumo_acucar = f"""
        <tr> 
            <th class="COLUNA_TOTAL NOME__TERMINAL">TOTAL RUMO AÇÚCAR</th>  
            <td class="TOTAL_{dia_logistico}">      { rumo_acucar["SALDOS"]["P1"]        }</td>
            <td class="TOTAL_{dia_logistico}">      { rumo_acucar["RECEBIMENTOS"]["P1"]  }</td>
            <td class="TOTAL_PD{dia_logistico}">    { rumo_acucar["PEDRA"]["P1"]         }</td> 

            <td class="TOTAL_{dia_logistico}">      { rumo_acucar["SALDOS"]["P2"]        }</td>
            <td class="TOTAL_{dia_logistico}">      { rumo_acucar["RECEBIMENTOS"]["P2"]  }</td>
            <td class="TOTAL_PD{dia_logistico}">    { rumo_acucar["PEDRA"]["P2"]         }</td>

            <td class="TOTAL_{dia_logistico}">      { rumo_acucar["SALDOS"]["P3"]        }</td>
            <td class="TOTAL_{dia_logistico}">      { rumo_acucar["RECEBIMENTOS"]["P3"]  }</td>
            <td class="TOTAL_PD{dia_logistico}">    { rumo_acucar["PEDRA"]["P3"]         }</td>

            <td class="TOTAL_{dia_logistico}">      { rumo_acucar["SALDOS"]["P4"]        }</td>
            <td class="TOTAL_{dia_logistico}">      { rumo_acucar["RECEBIMENTOS"]["P4"]  }</td>
            <td class="TOTAL_PD{dia_logistico}">    { rumo_acucar["PEDRA"]["P4"]         }</td>

            <td class="TOTAL_TOTAL{dia_logistico}"> { rumo_acucar["TT_OF"]  }</td>
            <td class="TOTAL_TOTAL{dia_logistico}"> { rumo_acucar["TT_PD"]  }</td>
        </tr> """

    rumo_celulose_psn = dict_relatorio_detalhe["RUMO"]["RUMO"]["CELULOSE"]['PSN'][dia_logistico]
    html_total_rumo_celulose_psn = ""
    if (int(rumo_celulose_psn["TT_OF"]) + int(rumo_celulose_psn["TT_PD"])) > 0:
        html_total_rumo_celulose_psn = f"""
        <tr>
            <th class="NOME__TERMINAL">RUMO CELULOSE PSN</th> 
            
            <td class="CONTEUDO_{dia_logistico}">   { rumo_celulose_psn["SALDOS"]["P1"]        }</td>
            <td class="CONTEUDO_{dia_logistico}">   { rumo_celulose_psn["RECEBIMENTOS"]["P1"]  }</td>
            <td class="CONTEUDO_PD{dia_logistico}"> { rumo_celulose_psn["PEDRA"]["P1"]         }</td> 

            <td class="CONTEUDO_{dia_logistico}">   { rumo_celulose_psn["SALDOS"]["P2"]        }</td>
            <td class="CONTEUDO_{dia_logistico}">   { rumo_celulose_psn["RECEBIMENTOS"]["P2"]  }</td>
            <td class="CONTEUDO_PD{dia_logistico}"> { rumo_celulose_psn["PEDRA"]["P2"]         }</td>

            <td class="CONTEUDO_{dia_logistico}">   { rumo_celulose_psn["SALDOS"]["P3"]        }</td>
            <td class="CONTEUDO_{dia_logistico}">   { rumo_celulose_psn["RECEBIMENTOS"]["P3"]  }</td>
            <td class="CONTEUDO_PD{dia_logistico}"> { rumo_celulose_psn["PEDRA"]["P3"]         }</td>

            <td class="CONTEUDO_{dia_logistico}">   { rumo_celulose_psn["SALDOS"]["P4"]        }</td>
            <td class="CONTEUDO_{dia_logistico}">   { rumo_celulose_psn["RECEBIMENTOS"]["P4"]  }</td>
            <td class="CONTEUDO_PD{dia_logistico}"> { rumo_celulose_psn["PEDRA"]["P4"]         }</td>

            <td class="COLUNA_TOTAL">{ rumo_celulose_psn["TT_OF"]  }</td>
            <td class="COLUNA_TOTAL">{ rumo_celulose_psn["TT_PD"]  }</td>
        </tr> """

    html_rumo = (
        
        html_total_rumo_graos_e_acucar  + 
        html_rumo_graos_psn             + 
        html_rumo_graos_pcz             + 
        html_total_rumo_graos           + 
        html_rumo_acucar_psn            + 
        html_rumo_acucar_pcz            + 
        html_total_rumo_acucar          +
        html_total_rumo_celulose_psn  
        
    )
    
    #endregion

    #region VLI
    
    vli_graos_psn = dict_relatorio_detalhe["VLI"]["GRAOS"]['PSN'][dia_logistico]
    html_vli_graos_psn = ""
    if (int(vli_graos_psn["TT_OF"]) + int(vli_graos_psn["TT_PD"])) > 0:
        html_vli_graos_psn = f"""
        <tr>
            <th class="NOME__TERMINAL">VLI GRÃOS PSN</th> 
            
            <td class="CONTEUDO_{dia_logistico}">   { vli_graos_psn["SALDOS"]["P1"]           }</td>
            <td class="CONTEUDO_{dia_logistico}">   { vli_graos_psn["RECEBIMENTOS"]["P1"]     }</td> 
            <td class="CONTEUDO_PD{dia_logistico}"> { vli_graos_psn["PEDRA"]["P1"]            }</td>  

            <td class="CONTEUDO_{dia_logistico}">   { vli_graos_psn["SALDOS"]["P2"]           }</td>
            <td class="CONTEUDO_{dia_logistico}">   { vli_graos_psn["RECEBIMENTOS"]["P2"]     }</td>
            <td class="CONTEUDO_PD{dia_logistico}"> { vli_graos_psn["PEDRA"]["P2"]            }</td>

            <td class="CONTEUDO_{dia_logistico}">   { vli_graos_psn["SALDOS"]["P3"]           }</td>
            <td class="CONTEUDO_{dia_logistico}">   { vli_graos_psn["RECEBIMENTOS"]["P3"]     }</td>
            <td class="CONTEUDO_PD{dia_logistico}"> { vli_graos_psn["PEDRA"]["P3"]            }</td>

            <td class="CONTEUDO_{dia_logistico}">   { vli_graos_psn["SALDOS"]["P4"]           }</td>
            <td class="CONTEUDO_{dia_logistico}">   { vli_graos_psn["RECEBIMENTOS"]["P4"]     }</td>
            <td class="CONTEUDO_PD{dia_logistico}"> { vli_graos_psn["PEDRA"]["P4"]            }</td>

            <td class="COLUNA_TOTAL">{ vli_graos_psn["TT_OF"]  }</td> 
            <td class="COLUNA_TOTAL">{ vli_graos_psn["TT_PD"]  }</td>
        </tr> """

    vli_graos_pcz = dict_relatorio_detalhe["VLI"]["GRAOS"]['PCZ'][dia_logistico]
    html_vli_graos_pcz = ""
    if (int(vli_graos_pcz["TT_OF"]) + int(vli_graos_pcz["TT_PD"])) > 0:
        html_vli_graos_pcz = f"""
        <tr>
            <th class="NOME__TERMINAL">VLI GRÃOS PCZ</th> 
            
            <td class="CONTEUDO_{dia_logistico}">   { vli_graos_pcz["SALDOS"]["P1"]           }</td>
            <td class="CONTEUDO_{dia_logistico}">   { vli_graos_pcz["RECEBIMENTOS"]["P1"]     }</td> 
            <td class="CONTEUDO_PD{dia_logistico}"> { vli_graos_pcz["PEDRA"]["P1"]            }</td>  

            <td class="CONTEUDO_{dia_logistico}">   { vli_graos_pcz["SALDOS"]["P2"]           }</td>
            <td class="CONTEUDO_{dia_logistico}">   { vli_graos_pcz["RECEBIMENTOS"]["P2"]     }</td>
            <td class="CONTEUDO_PD{dia_logistico}"> { vli_graos_pcz["PEDRA"]["P2"]            }</td>

            <td class="CONTEUDO_{dia_logistico}">   { vli_graos_pcz["SALDOS"]["P3"]           }</td>
            <td class="CONTEUDO_{dia_logistico}">   { vli_graos_pcz["RECEBIMENTOS"]["P3"]     }</td>
            <td class="CONTEUDO_PD{dia_logistico}"> { vli_graos_pcz["PEDRA"]["P3"]            }</td>

            <td class="CONTEUDO_{dia_logistico}">   { vli_graos_pcz["SALDOS"]["P4"]           }</td>
            <td class="CONTEUDO_{dia_logistico}">   { vli_graos_pcz["RECEBIMENTOS"]["P4"]     }</td>
            <td class="CONTEUDO_PD{dia_logistico}"> { vli_graos_pcz["PEDRA"]["P4"]            }</td>

            <td class="COLUNA_TOTAL">{ vli_graos_pcz["TT_OF"]  }</td> 
            <td class="COLUNA_TOTAL">{ vli_graos_pcz["TT_PD"]  }</td>
        </tr> """

    vli_acucar_psn = dict_relatorio_detalhe["VLI"]["ACUCAR"]['PSN'][dia_logistico]
    html_vli_acucar_psn = ""
    if (int(vli_acucar_psn["TT_OF"]) + int(vli_acucar_psn["TT_PD"])) > 0:
        html_vli_acucar_psn = f"""
        <tr>
            <th class="NOME__TERMINAL">VLI AÇÚCAR PSN</th> 
            
            <td class="CONTEUDO_{dia_logistico}">   { vli_acucar_psn["SALDOS"]["P1"]           }</td>
            <td class="CONTEUDO_{dia_logistico}">   { vli_acucar_psn["RECEBIMENTOS"]["P1"]     }</td> 
            <td class="CONTEUDO_PD{dia_logistico}"> { vli_acucar_psn["PEDRA"]["P1"]            }</td>  

            <td class="CONTEUDO_{dia_logistico}">   { vli_acucar_psn["SALDOS"]["P2"]           }</td>
            <td class="CONTEUDO_{dia_logistico}">   { vli_acucar_psn["RECEBIMENTOS"]["P2"]     }</td>
            <td class="CONTEUDO_PD{dia_logistico}"> { vli_acucar_psn["PEDRA"]["P2"]            }</td>

            <td class="CONTEUDO_{dia_logistico}">   { vli_acucar_psn["SALDOS"]["P3"]           }</td>
            <td class="CONTEUDO_{dia_logistico}">   { vli_acucar_psn["RECEBIMENTOS"]["P3"]     }</td>
            <td class="CONTEUDO_PD{dia_logistico}"> { vli_acucar_psn["PEDRA"]["P3"]            }</td>

            <td class="CONTEUDO_{dia_logistico}">   { vli_acucar_psn["SALDOS"]["P4"]           }</td>
            <td class="CONTEUDO_{dia_logistico}">   { vli_acucar_psn["RECEBIMENTOS"]["P4"]     }</td>
            <td class="CONTEUDO_PD{dia_logistico}"> { vli_acucar_psn["PEDRA"]["P4"]            }</td>

            <td class="COLUNA_TOTAL">{ vli_acucar_psn["TT_OF"]  }</td> 
            <td class="COLUNA_TOTAL">{ vli_acucar_psn["TT_PD"]  }</td>
        </tr> """

    vli_acucar_pcz = dict_relatorio_detalhe["VLI"]["ACUCAR"]['PCZ'][dia_logistico]
    html_vli_acucar_pcz = ""
    if (int(vli_acucar_pcz["TT_OF"]) + int(vli_acucar_pcz["TT_PD"])) > 0:
        html_vli_acucar_pcz = f"""
        <tr>
            <th class="NOME__TERMINAL">VLI AÇÚCAR PCZ</th> 
            
            <td class="CONTEUDO_{dia_logistico}">   { vli_acucar_pcz["SALDOS"]["P1"]           }</td>
            <td class="CONTEUDO_{dia_logistico}">   { vli_acucar_pcz["RECEBIMENTOS"]["P1"]     }</td> 
            <td class="CONTEUDO_PD{dia_logistico}"> { vli_acucar_pcz["PEDRA"]["P1"]            }</td>  

            <td class="CONTEUDO_{dia_logistico}">   { vli_acucar_pcz["SALDOS"]["P2"]           }</td>
            <td class="CONTEUDO_{dia_logistico}">   { vli_acucar_pcz["RECEBIMENTOS"]["P2"]     }</td>
            <td class="CONTEUDO_PD{dia_logistico}"> { vli_acucar_pcz["PEDRA"]["P2"]            }</td>

            <td class="CONTEUDO_{dia_logistico}">   { vli_acucar_pcz["SALDOS"]["P3"]           }</td>
            <td class="CONTEUDO_{dia_logistico}">   { vli_acucar_pcz["RECEBIMENTOS"]["P3"]     }</td>
            <td class="CONTEUDO_PD{dia_logistico}"> { vli_acucar_pcz["PEDRA"]["P3"]            }</td>

            <td class="CONTEUDO_{dia_logistico}">   { vli_acucar_pcz["SALDOS"]["P4"]           }</td>
            <td class="CONTEUDO_{dia_logistico}">   { vli_acucar_pcz["RECEBIMENTOS"]["P4"]     }</td>
            <td class="CONTEUDO_PD{dia_logistico}"> { vli_acucar_pcz["PEDRA"]["P4"]            }</td>

            <td class="COLUNA_TOTAL">{ vli_acucar_pcz["TT_OF"]  }</td> 
            <td class="COLUNA_TOTAL">{ vli_acucar_pcz["TT_PD"]  }</td>
        </tr> """ 

    vli_grao_e_acucar_psn = dict_relatorio_detalhe["VLI"]["TOTAO_GRAO_ACUCAR"][dia_logistico]
    html__total_vli_grao_e_acucar_psn = ""
    if (int(vli_grao_e_acucar_psn["TT_OF"]) + int(vli_grao_e_acucar_psn["TT_PD"])) > 0:
        html__total_vli_grao_e_acucar_psn = f"""
        <tr> 
            <th class="COLUNA_TOTAL NOME__TERMINAL">TOTAL VLI GRÃOS E AÇÚCAR PSN</th>  
            <td class="TOTAL_{dia_logistico}">      { vli_grao_e_acucar_psn["SALDOS"]["P1"]        }</td>
            <td class="TOTAL_{dia_logistico}">      { vli_grao_e_acucar_psn["RECEBIMENTOS"]["P1"]  }</td>
            <td class="TOTAL_PD{dia_logistico}">    { vli_grao_e_acucar_psn["PEDRA"]["P1"]         }</td> 

            <td class="TOTAL_{dia_logistico}">      { vli_grao_e_acucar_psn["SALDOS"]["P2"]        }</td>
            <td class="TOTAL_{dia_logistico}">      { vli_grao_e_acucar_psn["RECEBIMENTOS"]["P2"]  }</td>
            <td class="TOTAL_PD{dia_logistico}">    { vli_grao_e_acucar_psn["PEDRA"]["P2"]         }</td>

            <td class="TOTAL_{dia_logistico}">      { vli_grao_e_acucar_psn["SALDOS"]["P3"]        }</td>
            <td class="TOTAL_{dia_logistico}">      { vli_grao_e_acucar_psn["RECEBIMENTOS"]["P3"]  }</td>
            <td class="TOTAL_PD{dia_logistico}">    { vli_grao_e_acucar_psn["PEDRA"]["P3"]         }</td>

            <td class="TOTAL_{dia_logistico}">      { vli_grao_e_acucar_psn["SALDOS"]["P4"]        }</td>
            <td class="TOTAL_{dia_logistico}">      { vli_grao_e_acucar_psn["RECEBIMENTOS"]["P4"]  }</td>
            <td class="TOTAL_PD{dia_logistico}">    { vli_grao_e_acucar_psn["PEDRA"]["P4"]         }</td>

            <td class="TOTAL_TOTAL{dia_logistico}"> { vli_grao_e_acucar_psn["TT_OF"]  }</td>
            <td class="TOTAL_TOTAL{dia_logistico}"> { vli_grao_e_acucar_psn["TT_PD"]  }</td>
        </tr> """


    html_vli = (html_vli_graos_psn + html_vli_graos_pcz + html_vli_acucar_psn + html_vli_acucar_pcz + html__total_vli_grao_e_acucar_psn)
    #endregion

    #region TOTAIS
    totais_graos_psn = dict_relatorio_detalhe["TOTAIS"]["PSN"][dia_logistico]
    html_totais_graos_psn = f"""
    <tr>
        <th class="NOME__TERMINAL">TOTAIS GRÃOS PSN</th> 
          
        <td class="CONTEUDO_{dia_logistico}">   { totais_graos_psn["SALDOS"]["P1"]           }</td>
        <td class="CONTEUDO_{dia_logistico}">   { totais_graos_psn["RECEBIMENTOS"]["P1"]     }</td> 
        <td class="CONTEUDO_PD{dia_logistico}"> { totais_graos_psn["PEDRA"]["P1"]            }</td>  

        <td class="CONTEUDO_{dia_logistico}">   { totais_graos_psn["SALDOS"]["P2"]           }</td>
        <td class="CONTEUDO_{dia_logistico}">   { totais_graos_psn["RECEBIMENTOS"]["P2"]     }</td>
        <td class="CONTEUDO_PD{dia_logistico}"> { totais_graos_psn["PEDRA"]["P2"]            }</td>

        <td class="CONTEUDO_{dia_logistico}">   { totais_graos_psn["SALDOS"]["P3"]           }</td>
        <td class="CONTEUDO_{dia_logistico}">   { totais_graos_psn["RECEBIMENTOS"]["P3"]     }</td>
        <td class="CONTEUDO_PD{dia_logistico}"> { totais_graos_psn["PEDRA"]["P3"]            }</td>

        <td class="CONTEUDO_{dia_logistico}">   { totais_graos_psn["SALDOS"]["P4"]           }</td>
        <td class="CONTEUDO_{dia_logistico}">   { totais_graos_psn["RECEBIMENTOS"]["P4"]     }</td>
        <td class="CONTEUDO_PD{dia_logistico}"> { totais_graos_psn["PEDRA"]["P4"]            }</td>

        <td class="COLUNA_TOTAL">{ totais_graos_psn["TT_OF"]  }</td> 
        <td class="COLUNA_TOTAL">{ totais_graos_psn["TT_PD"]  }</td>
    </tr> """

    totais_graos_pcz = dict_relatorio_detalhe["TOTAIS"]["PCZ"][dia_logistico]
    html_totais_graos_pcz = f"""
    <tr>
        <th class="NOME__TERMINAL">TOTAIS GRÃOS PCZ</th> 
          
        <td class="CONTEUDO_{dia_logistico}">   { totais_graos_pcz["SALDOS"]["P1"]           }</td>
        <td class="CONTEUDO_{dia_logistico}">   { totais_graos_pcz["RECEBIMENTOS"]["P1"]     }</td> 
        <td class="CONTEUDO_PD{dia_logistico}"> { totais_graos_pcz["PEDRA"]["P1"]            }</td>  

        <td class="CONTEUDO_{dia_logistico}">   { totais_graos_pcz["SALDOS"]["P2"]           }</td>
        <td class="CONTEUDO_{dia_logistico}">   { totais_graos_pcz["RECEBIMENTOS"]["P2"]     }</td>
        <td class="CONTEUDO_PD{dia_logistico}"> { totais_graos_pcz["PEDRA"]["P2"]            }</td>

        <td class="CONTEUDO_{dia_logistico}">   { totais_graos_pcz["SALDOS"]["P3"]           }</td>
        <td class="CONTEUDO_{dia_logistico}">   { totais_graos_pcz["RECEBIMENTOS"]["P3"]     }</td>
        <td class="CONTEUDO_PD{dia_logistico}"> { totais_graos_pcz["PEDRA"]["P3"]            }</td>

        <td class="CONTEUDO_{dia_logistico}">   { totais_graos_pcz["SALDOS"]["P4"]           }</td>
        <td class="CONTEUDO_{dia_logistico}">   { totais_graos_pcz["RECEBIMENTOS"]["P4"]     }</td>
        <td class="CONTEUDO_PD{dia_logistico}"> { totais_graos_pcz["PEDRA"]["P4"]            }</td>

        <td class="COLUNA_TOTAL">{ totais_graos_pcz["TT_OF"]  }</td> 
        <td class="COLUNA_TOTAL">{ totais_graos_pcz["TT_PD"]  }</td>
    </tr> """

        
    totais_graos_e_acucar = dict_relatorio_detalhe["TOTAIS"]["GRAO_ACUCAR"][dia_logistico]
    html_totais_graos_e_acucar = f"""
    <tr> 
        <th class="COLUNA_TOTAL NOME__TERMINAL">TOTAL GRÃOS E AÇÚCAR</th>  
        <td class="TOTAL_{dia_logistico}">      { totais_graos_e_acucar["SALDOS"]["P1"]        }</td>
        <td class="TOTAL_{dia_logistico}">      { totais_graos_e_acucar["RECEBIMENTOS"]["P1"]  }</td>
        <td class="TOTAL_PD{dia_logistico}">    { totais_graos_e_acucar["PEDRA"]["P1"]         }</td> 

        <td class="TOTAL_{dia_logistico}">      { totais_graos_e_acucar["SALDOS"]["P2"]        }</td>
        <td class="TOTAL_{dia_logistico}">      { totais_graos_e_acucar["RECEBIMENTOS"]["P2"]  }</td>
        <td class="TOTAL_PD{dia_logistico}">    { totais_graos_e_acucar["PEDRA"]["P2"]         }</td>

        <td class="TOTAL_{dia_logistico}">      { totais_graos_e_acucar["SALDOS"]["P3"]        }</td>
        <td class="TOTAL_{dia_logistico}">      { totais_graos_e_acucar["RECEBIMENTOS"]["P3"]  }</td>
        <td class="TOTAL_PD{dia_logistico}">    { totais_graos_e_acucar["PEDRA"]["P3"]         }</td>

        <td class="TOTAL_{dia_logistico}">      { totais_graos_e_acucar["SALDOS"]["P4"]        }</td>
        <td class="TOTAL_{dia_logistico}">      { totais_graos_e_acucar["RECEBIMENTOS"]["P4"]  }</td>
        <td class="TOTAL_PD{dia_logistico}">    { totais_graos_e_acucar["PEDRA"]["P4"]         }</td>

        <td class="TOTAL_TOTAL{dia_logistico}"> { totais_graos_e_acucar["TT_OF"]  }</td>
        <td class="TOTAL_TOTAL{dia_logistico}"> { totais_graos_e_acucar["TT_PD"]  }</td>
    </tr> """

    totais_geral = dict_relatorio_detalhe["TOTAIS"]["GERAL"][dia_logistico]
    html_totais_geral = f"""
    <tr> 
        <th class="COLUNA_TOTAL NOME__TERMINAL">TOTAL GERAL FERROVIAS</th>  
        <td class="TOTAL_{dia_logistico}">      { totais_geral["SALDOS"]["P1"]        }</td>
        <td class="TOTAL_{dia_logistico}">      { totais_geral["RECEBIMENTOS"]["P1"]  }</td>
        <td class="TOTAL_PD{dia_logistico}">    { totais_geral["PEDRA"]["P1"]         }</td> 

        <td class="TOTAL_{dia_logistico}">      { totais_geral["SALDOS"]["P2"]        }</td>
        <td class="TOTAL_{dia_logistico}">      { totais_geral["RECEBIMENTOS"]["P2"]  }</td>
        <td class="TOTAL_PD{dia_logistico}">    { totais_geral["PEDRA"]["P2"]         }</td>

        <td class="TOTAL_{dia_logistico}">      { totais_geral["SALDOS"]["P3"]        }</td>
        <td class="TOTAL_{dia_logistico}">      { totais_geral["RECEBIMENTOS"]["P3"]  }</td>
        <td class="TOTAL_PD{dia_logistico}">    { totais_geral["PEDRA"]["P3"]         }</td>

        <td class="TOTAL_{dia_logistico}">      { totais_geral["SALDOS"]["P4"]        }</td>
        <td class="TOTAL_{dia_logistico}">      { totais_geral["RECEBIMENTOS"]["P4"]  }</td>
        <td class="TOTAL_PD{dia_logistico}">    { totais_geral["PEDRA"]["P4"]         }</td>

        <td class="TOTAL_TOTAL{dia_logistico}"> { totais_geral["TT_OF"]  }</td>
        <td class="TOTAL_TOTAL{dia_logistico}"> { totais_geral["TT_PD"]  }</td>
    </tr> """

    totais_fips =  html_totais_graos_psn + html_totais_graos_pcz + html_totais_graos_e_acucar + html_totais_geral

    #endregion
    
    html_detalhe = (
            html_detalhe_header + 
            html_mrs            + 
            PULA_LINHA          + 
            html_rumo           + 
            PULA_LINHA          + 
            html_vli            + 
            PULA_LINHA          + 
            totais_fips         +
            "</table>"
        )

    html_detalhe = html_detalhe.replace(">0</td>", "></td>")
    html_detalhe = html_detalhe.replace(" 0</td>", "</td>")
    return html_detalhe

def totais_detalhe(dia_logistico):
    
    dias_logisticos = ["D", "D+1", "D+2"]
    dia_logistico = dias_logisticos.index(dia_logistico)

    dict_relatorio_detalhe = criar_relatorio_detalhe()
    
    del dict_relatorio_detalhe["PRINCIPAL"]
 
    html = montar_html_detalhe(dict_relatorio_detalhe, dia_logistico)
    
    return html