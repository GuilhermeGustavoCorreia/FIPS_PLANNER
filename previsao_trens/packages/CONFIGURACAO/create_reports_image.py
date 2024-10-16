import imgkit



from previsao_trens.packages.DETELHE.CARREGAR_PAGINA import CARREGAR_RELATORIO_DETALHE as criar_relatorio_detalhe

def imagem_detalhe(dia_logistico):

    css_style = """ 
    table{ 
            font-family: Arial;
            border-collapse: collapse;
        }
        table  th   {border:     1px black solid}

        table td, th{ 
            
            text-align: center;
            padding:    0 1rem;
        }

        table tr{height: 1rem;}

        body{
            margin:       0 auto;
            user-select:    none;
            display:        flex;
            cursor:      default;
            overflow:     hidden;
            background-color: white;

        }
        .NOME__TERMINAL{ 
            border: 1px black solid;
            min-width: 6rem;
            text-align: left;
        }

        .COLUNA_TOTAL{
            background-color: #C0CCD2;
            border-left: 1px solid black; 
            border-right: 1px solid black;
        }

        .TOTAL_TOTAL0,.TOTAL_TOTAL2, .TOTAL_TOTAL4{ 
            border:    1px solid black; 
            background-color: #658EC9;
        }
        .TOTAL_0, .TOTAL_2, .TOTAL_4{
            background-color: #93BDE4;;
            border-left: none;
            border-right: none;
            border-top: 1px solid black;
            border-bottom: 1px solid black; 
            
        }

        .TOTAL_PD0, .TOTAL_PD2, .TOTAL_PD4  {
            background-color: #658EC9;
            border: 1px solid black;
        }

        .CONTEUDO_0, .CONTEUDO_2, .CONTEUDO_4{
            background-color: #D3E3F4;
            border-left:     1px solid #C0CCD2;
        }


        .CONTEUDO_PD0, .CONTEUDO_PD2, .CONTEUDO_PD4{
            background-color: #93BDE4;;
            border-left: 1px solid black;
            border-right: 1px solid black;
        }

        .CONTEUDO_PD1, .CONTEUDO_PD3{
            background-color: var(--verde-floresta-c);
            border-left: 1px solid black;
            border-right: 1px solid black;
        }

        .TOTAL_PD1, .TOTAL_PD3{
            background-color: var(--verde-floresta-m);
            border: 1px solid black;
            color: white;
        }

        .TOTAL_1, .TOTAL_3{
            background-color: var(--verde-floresta-c);
            border-left: none;
            border-right: none;
            border-top: 1px solid black;
            border-bottom: 1px solid black; 
            
        }

        .TOTAL_TOTAL1, .TOTAL_TOTAL3{ 
            border:    1px solid black; 
            background-color: var(--verde-floresta-m);
            color: white;
        }

        .CONTEUDO_1, .CONTEUDO_3{
            background-color: #dde7e1;
            border-left:     1px solid var(--cinza-chumbo-m);
        }


        .TITULO_AZUL    {background-color: #658EC9; color: white}
        .TITULO_VERDE   {background-color: var(--verde-floresta-c); color:white}

        .SEM_NAVEGACAO{

            height: fit-content;
            margin: auto;
            text-align: center;
        }

        .SEM_NAVEGACAO img{

            width: 20%;
        }

        .PULA_LINHA{
            color:transparent;
            border-top: 1px black solid !important;
            border-bottom: 1px black solid !important;
        }

        .border_bottom{ border-bottom: 1px black solid ;}

        .border_top{ border-top: 1px black solid ;}
    """

    detailed_report = criar_relatorio_detalhe()
    
    table_header = """   
            <table>
                <thead>
                    <tr>
                        
                        <th class="CELULA_VAZIA" colspan=4 rowspan=3>    
                        </th>

                        <th colspan=14 class="TITULO_AZUL">
                            PREVISÃO D
                        </th>
                    
                    </tr>
                    
                    <tr>

                        <th colspan=3>
                            01h-07h
                        </th>
                        <th colspan=3>
                            07h-13h
                        </th>
                        <th colspan=3>
                            13h-19h
                        </th>
                        <th colspan=3>
                            19h-01h
                        </th>

                        <th colspan=2>
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

    str_html = ""
    #region POR TERMINAL
    for  NOME_TERMINAL, DADOS in detailed_report["PRINCIPAL"].items():    
        
        for NOME_FERROVIA, DADOS_FERROVIA in DADOS.items():
            
            if not NOME_FERROVIA == "MARGEM" and not NOME_FERROVIA == "TOTAL": 

                for NOME_PRODUTO, DADOS_PRODUTO in DADOS_FERROVIA.items():
                    
                    #region UMA LINHA 
                    str_html += f"""
                    <tr>
                            <th class="NOME__TERMINAL">
                                {DADOS["MARGEM"]}
                            </th>
                            <th class="NOME__TERMINAL">
                                {NOME_TERMINAL} 
                            </th>
                            <th class="NOME__FERROVIA">
                                {NOME_FERROVIA}
                            </th>
                            <th class="NM_PRODUTO">
                                {NOME_PRODUTO}
                            </th>
                            """
                    
                    for DIA_LOGISTICO, DADOS_DIA_LOGISTICO in DADOS_PRODUTO.items():
                        if DIA_LOGISTICO == dia_logistico:

                             

                            str_html += f"""<td class="CONTEUDO_{DIA_LOGISTICO}">"""

                            if DADOS_DIA_LOGISTICO["SALDOS"]["P1"] != 0:                   
                                str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P1"])
                                        
                            str_html += "</td>"  

                            str_html += f"""<td class="CONTEUDO_{DIA_LOGISTICO}">"""

                            if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P1"] != 0:                    
                                str_html += str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P1"]) 
                                        
                            str_html += "</td>" 
                                    
                            str_html += f"""<td class="CONTEUDO_PD{DIA_LOGISTICO}">"""  

                            if DADOS_DIA_LOGISTICO["PEDRA"]["P1"] != 0:                     
                                str_html += str(DADOS_DIA_LOGISTICO["PEDRA"]["P1"]) 
                                        
                            str_html += "</td>"

                            str_html += f"""<td class="CONTEUDO_{DIA_LOGISTICO}">"""

                            if DADOS_DIA_LOGISTICO["SALDOS"]["P2"] != 0:                     
                                str_html +=  str(DADOS_DIA_LOGISTICO["SALDOS"]["P2"]) 
                                            
                            str_html += "</td>"        
    
                            str_html += f"""<td class="CONTEUDO_{DIA_LOGISTICO}">"""
                                        
                            if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P2"] != 0:                       
                                str_html +=  str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P2"]) 
                                            
                            str_html += "</td>" 

                            str_html += f"""<td class="CONTEUDO_PD{DIA_LOGISTICO}">"""     
                                        
                            if DADOS_DIA_LOGISTICO["PEDRA"]["P2"] != 0 :                      
                                str_html += str(DADOS_DIA_LOGISTICO["PEDRA"]["P2"])
                                        
                            str_html += "</td>" 


                            str_html += f"""<td class="CONTEUDO_{DIA_LOGISTICO}">"""

                            if DADOS_DIA_LOGISTICO["SALDOS"]["P3"] != 0:                       
                                str_html += str(DADOS_DIA_LOGISTICO["SALDOS"]["P3"])
                                        

                            str_html += "</td>" 
                            
                            str_html += f"""<td class="CONTEUDO_{DIA_LOGISTICO}">"""

                            if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P3"] != 0:                       
                                str_html += str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P3"]) 
                                        
                            str_html += "</td>" 

                            str_html += f"""<td class="CONTEUDO_PD{DIA_LOGISTICO}">"""

                            if DADOS_DIA_LOGISTICO["PEDRA"]["P3"] != 0:                       
                                str_html += str(DADOS_DIA_LOGISTICO["PEDRA"]["P3"])
                                        
                            str_html += "</td>"

                            str_html += f"""<td class="CONTEUDO_{DIA_LOGISTICO}">"""
                                        
                            if DADOS_DIA_LOGISTICO["SALDOS"]["P4"] != 0:                       
                                str_html += str(DADOS_DIA_LOGISTICO["SALDOS"]["P4"]) 
                                        
                            str_html += "</td>"
                                
                            str_html += f"""<td class="CONTEUDO_{DIA_LOGISTICO}">"""
        
                            if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P4"] != 0:                       
                                str_html += str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P4"])
                                        
                            str_html += f"""<td class="CONTEUDO_PD{DIA_LOGISTICO}">"""
                                        
                            if DADOS_DIA_LOGISTICO["PEDRA"]["P4"] != 0:                       
                                str_html += str(DADOS_DIA_LOGISTICO["PEDRA"]["P4"])
                                        
                            str_html += "</td>"   

                            str_html += f"""<td class="COLUNA_TOTAL">"""

                            if DADOS_DIA_LOGISTICO["TT_OF"] != 0:                       
                                str_html += str(DADOS_DIA_LOGISTICO["TT_OF"])
                                        
                            str_html += "</td>"


                            str_html += f"""<td class="COLUNA_TOTAL">"""

                            if DADOS_DIA_LOGISTICO["TT_PD"] != 0:                     
                                str_html += str(DADOS_DIA_LOGISTICO["TT_PD"])
                                        

                            str_html += "</td>"

                    #endregion

                    str_html += "</tr>"
        #region LINHA TOTAL DE CADA TERMINAL
        str_html += "<tr class='TOTAL'> "
        
        str_html +=f"""<th colspan=4 class="NOME__TERMINAL COLUNA_TOTAL">{NOME_TERMINAL} TOTAL</th> """
                
        for DIA_LOGISTICO, DADOS_DIA_LOGISTICO in DADOS["TOTAL"].items():
            print(DADOS_DIA_LOGISTICO)                
            if DIA_LOGISTICO == dia_logistico:

                str_html +=f"""<td class="TOTAL_{DIA_LOGISTICO}">"""                    
                        
                if DADOS_DIA_LOGISTICO["SALDOS"]["P1"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P1"])
                            

                str_html += "</td>"  
                str_html += f"""<td class="TOTAL_{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P1"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P1"])
                            

                str_html += "</td>" 
                str_html += f"""<td class="TOTAL_PD{DIA_LOGISTICO}">"""
                        
                if DADOS_DIA_LOGISTICO["PEDRA"]["P1"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P1"]) 
                            
                str_html += "</td>"

                str_html += f"""<td class="TOTAL_{DIA_LOGISTICO}">"""  
                        
                if DADOS_DIA_LOGISTICO["SALDOS"]["P2"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P2"])
                            
                str_html += "</td>"

                str_html += f"""<td class="TOTAL_{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P2"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P2"])
                            
                str_html += "</td>"

                str_html += f"""<td class="TOTAL_PD{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["PEDRA"]["P2"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P2"]) 
                            
                str_html += "</td>"
                    
                str_html += f"""<td class="TOTAL_{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["SALDOS"]["P3"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P3"]) 
                                

                str_html += "</td>"
                str_html += f"""<td class="TOTAL_{DIA_LOGISTICO}">"""
                        
                if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P3"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P3"]) 
                                

                str_html += "</td>"
                str_html += f"""<td class="TOTAL_PD{DIA_LOGISTICO}">"""
                            
                if DADOS_DIA_LOGISTICO["PEDRA"]["P3"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P3"])
                                
                str_html += "</td>"
                    

                str_html += f"""<td class="TOTAL_{DIA_LOGISTICO}">"""
                        
                if DADOS_DIA_LOGISTICO["SALDOS"]["P4"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P4"])
                                

                str_html += "</td>"
                str_html += f"""<td class="TOTAL_{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P4"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P4"]) 
                                

                str_html += "</td>" 
                str_html += f"""<td class="TOTAL_PD{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["PEDRA"]["P4"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P4"])
                                
                str_html += "</td>"
                    
                str_html += f"""<td class="TOTAL_TOTAL{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["TT_OF"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["TT_OF"]) 
                            

                str_html += "</td>" 
                str_html += f"""<td class="TOTAL_TOTAL{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["TT_PD"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["TT_PD"]) 
                            

                str_html += "</td>"
                    
        
        str_html += "</tr>"
    #endregion

    #endregion

    str_html += """<tr><td colspan="72" CLASS="PULA_LINHA">.</td></tr>"""

    #region RELATORIO RUMO

    #region RELATORIO RUMO TOTAL GRAO + ACUCAR

    str_html += """<tr class="TOTAL">"""
    str_html += """<th colspan="4" class=" COLUNA_TOTAL NOME__TERMINAL">TOTAL RUMO GRÃOS E AÇÚCAR</th>"""

    for DIA_LOGISTICO, DADOS_DIA_LOGISTICO in  detailed_report["RUMO"]["RUMO"]["TOTAO_GRAO_ACUCAR"].items():
            if DIA_LOGISTICO == dia_logistico:
                str_html += f""" <td class="TOTAL_{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["SALDOS"]["P1"] != 0:                    
                    str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P1"]) 
                        

                str_html += "</td>" 
                str_html += f""" <td class="TOTAL_{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P1"] != 0:                    
                    str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P1"]) 
                    

                str_html += "</td>"  
                str_html += f""" <td class="TOTAL_PD{DIA_LOGISTICO}">  """

                if DADOS_DIA_LOGISTICO["PEDRA"]["P1"] != 0:                    
                    str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P1"]) 
                        

                str_html += "</td>"

                str_html += f""" <td class="TOTAL_{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["SALDOS"]["P2"] != 0:                    
                    str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P2"] )
                            
                    
                str_html += "</td>"
                str_html += f""" <td class="TOTAL_{DIA_LOGISTICO}">"""
                    
                if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P2"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P2"]) 
                            
                    
                str_html += "</td>"
                str_html += f""" <td class="TOTAL_PD{DIA_LOGISTICO}">"""     
                        
                if DADOS_DIA_LOGISTICO["PEDRA"]["P2"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P2"]) 
                        

                str_html += "</td>"
                str_html += f""" <td class="TOTAL_{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["SALDOS"]["P3"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P3"]) 
                        

                str_html += "</td>"
                str_html += f""" <td class="TOTAL_{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P3"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P3"]) 
                        

                str_html += "</td>"
                str_html += f""" <td class="TOTAL_PD{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["PEDRA"]["P3"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P3"]) 
                        

                str_html += "</td>"
                    

                str_html += f""" <td class="TOTAL_{DIA_LOGISTICO}">"""
                        
                if DADOS_DIA_LOGISTICO["SALDOS"]["P4"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P4"]) 
                        

                str_html += "</td>"
                str_html += f""" <td class="TOTAL_{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P4"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P4"]) 
                        
                    
                str_html += "</td>"
                str_html += f""" <td class="TOTAL_PD{DIA_LOGISTICO}">"""
                        
                if DADOS_DIA_LOGISTICO["PEDRA"]["P4"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P4"]) 
                        
                    
                str_html += "</td>"
                    
                    
                str_html += f""" <td class="TOTAL_TOTAL{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["TT_OF"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["TT_OF"])
                        

                str_html += "</td>"
                str_html += f""" <td class="TOTAL_TOTAL{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["TT_PD"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["TT_PD"]) 
                        

                str_html += "</td>"

            str_html += "</tr>"

    #endregion

    #region RELATORIO RUMO PSN-
    if detailed_report["RUMO"]["RUMO"]["GRAOS"]["PSN"]:
        
        
            str_html += "<tr>"

            str_html += f""" <th colspan="4" class="NOME__TERMINAL">RUMO GRÃO PSN</th>"""

            for DIA_LOGISTICO, DADOS_DIA_LOGISTICO in  detailed_report["RUMO"]["RUMO"]["GRAOS"]["PSN"].items():

                if DIA_LOGISTICO == dia_logistico:

                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["SALDOS"]["P1"] != 0:                    
                        str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P1"]) 
                    

                    str_html += "</td>"   
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P1"] != 0:                    
                        str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P1"])
                        

                    str_html += "</td>"   
                    str_html += f""" <td class="CONTEUDO_PD{DIA_LOGISTICO}">"""  

                    if DADOS_DIA_LOGISTICO["PEDRA"]["P1"] != 0:                    
                        str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P1"])
                        

                    str_html += "</td>" 

                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["SALDOS"]["P2"] != 0:                    
                        str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P2"])
                                
                    
                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""
                        
                    if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P2"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P2"])
                            
                    
                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_PD{DIA_LOGISTICO}">"""     
                        
                    if DADOS_DIA_LOGISTICO["PEDRA"]["P2"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P2"])
                            

                    str_html += "</td>" 
                    
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["SALDOS"]["P3"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P3"])
                            

                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P3"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P3"])
                            

                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_PD{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["PEDRA"]["P3"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P3"])
                            

                    str_html += "</td>" 
                    

                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""
                        
                    if DADOS_DIA_LOGISTICO["SALDOS"]["P4"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P4"])
                            

                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P4"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P4"])
                            
                    
                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_PD{DIA_LOGISTICO}">"""
                        
                    if DADOS_DIA_LOGISTICO["PEDRA"]["P4"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P4"])
                            
                    
                    str_html += "</td>" 
                    
                    
                    str_html += f""" <td class="COLUNA_TOTAL">"""

                    if DADOS_DIA_LOGISTICO["TT_OF"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["TT_OF"])
                            

                    str_html += "</td>"  
                    str_html += f""" <td class="COLUNA_TOTAL">"""

                    if DADOS_DIA_LOGISTICO["TT_PD"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["TT_PD"])
                            

                    str_html += "</td>" 
                
            str_html += "</tr>"       
    #endregion

    #region  RELATORIO RUMO PCZ
    if detailed_report["RUMO"]["RUMO"]["GRAOS"]["PCZ"]:
               
            str_html += "<tr>"

            str_html += f""" <th colspan="4" class="NOME__TERMINAL">RUMO GRÃO PCZ</th>"""

            for DIA_LOGISTICO, DADOS_DIA_LOGISTICO in  detailed_report["RUMO"]["RUMO"]["GRAOS"]["PCZ"].items():

                if DIA_LOGISTICO == dia_logistico:

                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["SALDOS"]["P1"] != 0:                    
                        str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P1"]) 
                    

                    str_html += "</td>"   
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P1"] != 0:                    
                        str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P1"])
                        

                    str_html += "</td>"   
                    str_html += f""" <td class="CONTEUDO_PD{DIA_LOGISTICO}">"""  

                    if DADOS_DIA_LOGISTICO["PEDRA"]["P1"] != 0:                    
                        str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P1"])
                        

                    str_html += "</td>" 

                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["SALDOS"]["P2"] != 0:                    
                        str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P2"])
                                
                    
                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""
                        
                    if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P2"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P2"])
                            
                    
                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_PD{DIA_LOGISTICO}">"""     
                        
                    if DADOS_DIA_LOGISTICO["PEDRA"]["P2"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P2"])
                            

                    str_html += "</td>" 
                    
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["SALDOS"]["P3"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P3"])
                            

                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P3"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P3"])
                            

                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_PD{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["PEDRA"]["P3"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P3"])
                            

                    str_html += "</td>" 
                    

                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""
                        
                    if DADOS_DIA_LOGISTICO["SALDOS"]["P4"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P4"])
                            

                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P4"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P4"])
                            
                    
                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_PD{DIA_LOGISTICO}">"""
                        
                    if DADOS_DIA_LOGISTICO["PEDRA"]["P4"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P4"])
                            
                    
                    str_html += "</td>" 
                    
                    
                    str_html += f""" <td class="COLUNA_TOTAL">"""

                    if DADOS_DIA_LOGISTICO["TT_OF"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["TT_OF"])
                            

                    str_html += "</td>"  
                    str_html += f""" <td class="COLUNA_TOTAL">"""

                    if DADOS_DIA_LOGISTICO["TT_PD"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["TT_PD"])
                            

                    str_html += "</td>" 
                
            str_html += "</tr>"       
    #endregion

    #region  RELATORIO RUMO TOTAIL GRAO

    str_html += """<tr class="TOTAL">"""
    str_html += """<th colspan="4" class=" COLUNA_TOTAL NOME__TERMINAL">TOTAL RUMO GRÃOS</th>"""

    for DIA_LOGISTICO, DADOS_DIA_LOGISTICO in  detailed_report["RUMO"]["RUMO"]["GRAOS"]["TOTAL_GRAO"].items():
            if DIA_LOGISTICO == dia_logistico:
                str_html += f""" <td class="TOTAL_{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["SALDOS"]["P1"] != 0:                    
                    str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P1"]) 
                        

                str_html += "</td>" 
                str_html += f""" <td class="TOTAL_{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P1"] != 0:                    
                    str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P1"]) 
                    

                str_html += "</td>"  
                str_html += f""" <td class="TOTAL_PD{DIA_LOGISTICO}">  """

                if DADOS_DIA_LOGISTICO["PEDRA"]["P1"] != 0:                    
                    str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P1"]) 
                        

                str_html += "</td>"

                str_html += f""" <td class="TOTAL_{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["SALDOS"]["P2"] != 0:                    
                    str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P2"] )
                            
                    
                str_html += "</td>"
                str_html += f""" <td class="TOTAL_{DIA_LOGISTICO}">"""
                    
                if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P2"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P2"]) 
                            
                    
                str_html += "</td>"
                str_html += f""" <td class="TOTAL_PD{DIA_LOGISTICO}">"""     
                        
                if DADOS_DIA_LOGISTICO["PEDRA"]["P2"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P2"]) 
                        

                str_html += "</td>"
                str_html += f""" <td class="TOTAL_{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["SALDOS"]["P3"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P3"]) 
                        

                str_html += "</td>"
                str_html += f""" <td class="TOTAL_{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P3"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P3"]) 
                        

                str_html += "</td>"
                str_html += f""" <td class="TOTAL_PD{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["PEDRA"]["P3"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P3"]) 
                        

                str_html += "</td>"
                    

                str_html += f""" <td class="TOTAL_{DIA_LOGISTICO}">"""
                        
                if DADOS_DIA_LOGISTICO["SALDOS"]["P4"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P4"]) 
                        

                str_html += "</td>"
                str_html += f""" <td class="TOTAL_{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P4"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P4"]) 
                        
                    
                str_html += "</td>"
                str_html += f""" <td class="TOTAL_PD{DIA_LOGISTICO}">"""
                        
                if DADOS_DIA_LOGISTICO["PEDRA"]["P4"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P4"]) 
                        
                    
                str_html += "</td>"
                    
                    
                str_html += f""" <td class="TOTAL_TOTAL{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["TT_OF"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["TT_OF"])
                        

                str_html += "</td>"
                str_html += f""" <td class="TOTAL_TOTAL{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["TT_PD"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["TT_PD"]) 
                        

                str_html += "</td>"

            str_html += "</tr>"


    #endregion

    #region  RELATORIO RUMO ACUCAR PSN-
    if detailed_report["RUMO"]["RUMO"]["ACUCAR"]["PSN"]:
        
        
            str_html += "<tr>"

            str_html += f""" <th colspan="4" class="NOME__TERMINAL">RUMO AÇÚCAR PSN</th>"""

            for DIA_LOGISTICO, DADOS_DIA_LOGISTICO in  detailed_report["RUMO"]["RUMO"]["ACUCAR"]["PSN"].items():

                if DIA_LOGISTICO == dia_logistico:

                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["SALDOS"]["P1"] != 0:                    
                        str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P1"]) 
                    

                    str_html += "</td>"   
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P1"] != 0:                    
                        str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P1"])
                        

                    str_html += "</td>"   
                    str_html += f""" <td class="CONTEUDO_PD{DIA_LOGISTICO}">"""  

                    if DADOS_DIA_LOGISTICO["PEDRA"]["P1"] != 0:                    
                        str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P1"])
                        

                    str_html += "</td>" 

                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["SALDOS"]["P2"] != 0:                    
                        str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P2"])
                                
                    
                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""
                        
                    if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P2"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P2"])
                            
                    
                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_PD{DIA_LOGISTICO}">"""     
                        
                    if DADOS_DIA_LOGISTICO["PEDRA"]["P2"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P2"])
                            

                    str_html += "</td>" 
                    
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["SALDOS"]["P3"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P3"])
                            

                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P3"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P3"])
                            

                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_PD{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["PEDRA"]["P3"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P3"])
                            

                    str_html += "</td>" 
                    

                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""
                        
                    if DADOS_DIA_LOGISTICO["SALDOS"]["P4"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P4"])
                            

                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P4"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P4"])
                            
                    
                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_PD{DIA_LOGISTICO}">"""
                        
                    if DADOS_DIA_LOGISTICO["PEDRA"]["P4"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P4"])
                            
                    
                    str_html += "</td>" 
                    
                    
                    str_html += f""" <td class="COLUNA_TOTAL">"""

                    if DADOS_DIA_LOGISTICO["TT_OF"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["TT_OF"])
                            

                    str_html += "</td>"  
                    str_html += f""" <td class="COLUNA_TOTAL">"""

                    if DADOS_DIA_LOGISTICO["TT_PD"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["TT_PD"])
                            

                    str_html += "</td>" 
                
            str_html += "</tr>"       
    #endregion

    #region  RELATORIO RUMO ACUCAR PCZ
    if detailed_report["RUMO"]["RUMO"]["ACUCAR"]["PCZ"]:
               
            str_html += "<tr>"

            str_html += f""" <th colspan="4" class="NOME__TERMINAL">RUMO AÇÚCAR PCZ</th>"""

            for DIA_LOGISTICO, DADOS_DIA_LOGISTICO in  detailed_report["RUMO"]["RUMO"]["ACUCAR"]["PCZ"].items():

                if DIA_LOGISTICO == dia_logistico:

                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["SALDOS"]["P1"] != 0:                    
                        str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P1"]) 
                    

                    str_html += "</td>"   
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P1"] != 0:                    
                        str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P1"])
                        

                    str_html += "</td>"   
                    str_html += f""" <td class="CONTEUDO_PD{DIA_LOGISTICO}">"""  

                    if DADOS_DIA_LOGISTICO["PEDRA"]["P1"] != 0:                    
                        str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P1"])
                        

                    str_html += "</td>" 

                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["SALDOS"]["P2"] != 0:                    
                        str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P2"])
                                
                    
                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""
                        
                    if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P2"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P2"])
                            
                    
                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_PD{DIA_LOGISTICO}">"""     
                        
                    if DADOS_DIA_LOGISTICO["PEDRA"]["P2"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P2"])
                            

                    str_html += "</td>" 
                    
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["SALDOS"]["P3"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P3"])
                            

                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P3"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P3"])
                            

                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_PD{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["PEDRA"]["P3"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P3"])
                            

                    str_html += "</td>" 
                    

                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""
                        
                    if DADOS_DIA_LOGISTICO["SALDOS"]["P4"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P4"])
                            

                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P4"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P4"])
                            
                    
                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_PD{DIA_LOGISTICO}">"""
                        
                    if DADOS_DIA_LOGISTICO["PEDRA"]["P4"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P4"])
                            
                    
                    str_html += "</td>" 
                    
                    
                    str_html += f""" <td class="COLUNA_TOTAL">"""

                    if DADOS_DIA_LOGISTICO["TT_OF"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["TT_OF"])
                            

                    str_html += "</td>"  
                    str_html += f""" <td class="COLUNA_TOTAL">"""

                    if DADOS_DIA_LOGISTICO["TT_PD"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["TT_PD"])
                            

                    str_html += "</td>" 
                
            str_html += "</tr>"       
    #endregion

    #region  RELATORIO RUMO TOTAL ACUCAR

    str_html += """<tr class="TOTAL">"""
    str_html += """<th colspan="4" class=" COLUNA_TOTAL NOME__TERMINAL">TOTAL RUMO AÇÚCAR</th>"""

    for DIA_LOGISTICO, DADOS_DIA_LOGISTICO in  detailed_report["RUMO"]["RUMO"]["ACUCAR"]["TOTAL_ACUCAR"].items():
            if DIA_LOGISTICO == dia_logistico:
                str_html += f""" <td class="TOTAL_{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["SALDOS"]["P1"] != 0:                    
                    str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P1"]) 
                        

                str_html += "</td>" 
                str_html += f""" <td class="TOTAL_{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P1"] != 0:                    
                    str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P1"]) 
                    

                str_html += "</td>"  
                str_html += f""" <td class="TOTAL_PD{DIA_LOGISTICO}">  """

                if DADOS_DIA_LOGISTICO["PEDRA"]["P1"] != 0:                    
                    str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P1"]) 
                        

                str_html += "</td>"

                str_html += f""" <td class="TOTAL_{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["SALDOS"]["P2"] != 0:                    
                    str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P2"] )
                            
                    
                str_html += "</td>"
                str_html += f""" <td class="TOTAL_{DIA_LOGISTICO}">"""
                    
                if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P2"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P2"]) 
                            
                    
                str_html += "</td>"
                str_html += f""" <td class="TOTAL_PD{DIA_LOGISTICO}">"""     
                        
                if DADOS_DIA_LOGISTICO["PEDRA"]["P2"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P2"]) 
                        

                str_html += "</td>"
                str_html += f""" <td class="TOTAL_{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["SALDOS"]["P3"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P3"]) 
                        

                str_html += "</td>"
                str_html += f""" <td class="TOTAL_{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P3"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P3"]) 
                        

                str_html += "</td>"
                str_html += f""" <td class="TOTAL_PD{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["PEDRA"]["P3"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P3"]) 
                        

                str_html += "</td>"
                    

                str_html += f""" <td class="TOTAL_{DIA_LOGISTICO}">"""
                        
                if DADOS_DIA_LOGISTICO["SALDOS"]["P4"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P4"]) 
                        

                str_html += "</td>"
                str_html += f""" <td class="TOTAL_{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P4"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P4"]) 
                        
                    
                str_html += "</td>"
                str_html += f""" <td class="TOTAL_PD{DIA_LOGISTICO}">"""
                        
                if DADOS_DIA_LOGISTICO["PEDRA"]["P4"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P4"]) 
                        
                    
                str_html += "</td>"
                    
                    
                str_html += f""" <td class="TOTAL_TOTAL{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["TT_OF"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["TT_OF"])
                        

                str_html += "</td>"
                str_html += f""" <td class="TOTAL_TOTAL{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["TT_PD"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["TT_PD"]) 
                        

                str_html += "</td>"

            str_html += "</tr>"


    #endregion

    #region  RELATORIO RUMO CELULOSE PSN-
    if detailed_report["RUMO"]["RUMO"]["CELULOSE"]["PSN"]:
        
        
            str_html += "<tr>"

            str_html += f""" <th colspan="4" class="NOME__TERMINAL">RUMO AÇÚCAR PSN</th>"""

            for DIA_LOGISTICO, DADOS_DIA_LOGISTICO in  detailed_report["RUMO"]["RUMO"]["CELULOSE"]["PSN"].items():

                if DIA_LOGISTICO == dia_logistico:

                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["SALDOS"]["P1"] != 0:                    
                        str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P1"]) 
                    

                    str_html += "</td>"   
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P1"] != 0:                    
                        str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P1"])
                        

                    str_html += "</td>"   
                    str_html += f""" <td class="CONTEUDO_PD{DIA_LOGISTICO}">"""  

                    if DADOS_DIA_LOGISTICO["PEDRA"]["P1"] != 0:                    
                        str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P1"])
                        

                    str_html += "</td>" 

                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["SALDOS"]["P2"] != 0:                    
                        str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P2"])
                                
                    
                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""
                        
                    if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P2"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P2"])
                            
                    
                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_PD{DIA_LOGISTICO}">"""     
                        
                    if DADOS_DIA_LOGISTICO["PEDRA"]["P2"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P2"])
                            

                    str_html += "</td>" 
                    
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["SALDOS"]["P3"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P3"])
                            

                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P3"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P3"])
                            

                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_PD{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["PEDRA"]["P3"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P3"])
                            

                    str_html += "</td>" 
                    

                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""
                        
                    if DADOS_DIA_LOGISTICO["SALDOS"]["P4"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P4"])
                            

                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P4"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P4"])
                            
                    
                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_PD{DIA_LOGISTICO}">"""
                        
                    if DADOS_DIA_LOGISTICO["PEDRA"]["P4"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P4"])
                            
                    
                    str_html += "</td>" 
                    
                    
                    str_html += f""" <td class="COLUNA_TOTAL">"""

                    if DADOS_DIA_LOGISTICO["TT_OF"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["TT_OF"])
                            

                    str_html += "</td>"  
                    str_html += f""" <td class="COLUNA_TOTAL">"""

                    if DADOS_DIA_LOGISTICO["TT_PD"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["TT_PD"])
                            

                    str_html += "</td>" 
                
            str_html += "</tr>"       
    #endregion

    #region  RELATORIO RUMO TOTAL CELULOSE

    str_html += """<tr class="TOTAL">"""
    str_html += """<th colspan="4" class=" COLUNA_TOTAL NOME__TERMINAL">TOTAL RUMO CELULOSE</th>"""

    for DIA_LOGISTICO, DADOS_DIA_LOGISTICO in  detailed_report["RUMO"]["RUMO"]["CELULOSE"]["TOTAL_CELULOSE"].items():
            if DIA_LOGISTICO == dia_logistico:
                str_html += f""" <td class="TOTAL_{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["SALDOS"]["P1"] != 0:                    
                    str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P1"]) 
                        

                str_html += "</td>" 
                str_html += f""" <td class="TOTAL_{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P1"] != 0:                    
                    str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P1"]) 
                    

                str_html += "</td>"  
                str_html += f""" <td class="TOTAL_PD{DIA_LOGISTICO}">  """

                if DADOS_DIA_LOGISTICO["PEDRA"]["P1"] != 0:                    
                    str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P1"]) 
                        

                str_html += "</td>"

                str_html += f""" <td class="TOTAL_{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["SALDOS"]["P2"] != 0:                    
                    str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P2"] )
                            
                    
                str_html += "</td>"
                str_html += f""" <td class="TOTAL_{DIA_LOGISTICO}">"""
                    
                if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P2"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P2"]) 
                            
                    
                str_html += "</td>"
                str_html += f""" <td class="TOTAL_PD{DIA_LOGISTICO}">"""     
                        
                if DADOS_DIA_LOGISTICO["PEDRA"]["P2"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P2"]) 
                        

                str_html += "</td>"
                str_html += f""" <td class="TOTAL_{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["SALDOS"]["P3"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P3"]) 
                        

                str_html += "</td>"
                str_html += f""" <td class="TOTAL_{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P3"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P3"]) 
                        

                str_html += "</td>"
                str_html += f""" <td class="TOTAL_PD{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["PEDRA"]["P3"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P3"]) 
                        

                str_html += "</td>"
                    

                str_html += f""" <td class="TOTAL_{DIA_LOGISTICO}">"""
                        
                if DADOS_DIA_LOGISTICO["SALDOS"]["P4"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P4"]) 
                        

                str_html += "</td>"
                str_html += f""" <td class="TOTAL_{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P4"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P4"]) 
                        
                    
                str_html += "</td>"
                str_html += f""" <td class="TOTAL_PD{DIA_LOGISTICO}">"""
                        
                if DADOS_DIA_LOGISTICO["PEDRA"]["P4"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P4"]) 
                        
                    
                str_html += "</td>"
                    
                    
                str_html += f""" <td class="TOTAL_TOTAL{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["TT_OF"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["TT_OF"])
                        

                str_html += "</td>"
                str_html += f""" <td class="TOTAL_TOTAL{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["TT_PD"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["TT_PD"]) 
                        

                str_html += "</td>"

            str_html += "</tr>"


    #endregion

    #endregion

    str_html += """<tr><td colspan="72" CLASS="PULA_LINHA">.</td></tr>"""

    #region RELATORIO VLI

    #region RELATORIO VLI GRAO PSN

    if "VLI" in detailed_report:
        
        if detailed_report["VLI"]["GRAOS"]["PSN"]:
    
            str_html += "<tr>"

            str_html += f""" <th colspan="4" class="NOME__TERMINAL">VLI GRÃO PSN</th>"""

            for DIA_LOGISTICO, DADOS_DIA_LOGISTICO in  detailed_report["VLI"]["GRAOS"]["PSN"].items():

                if DIA_LOGISTICO == dia_logistico:

                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["SALDOS"]["P1"] != 0:                    
                        str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P1"]) 
                    

                    str_html += "</td>"   
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P1"] != 0:                    
                        str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P1"])
                        

                    str_html += "</td>"   
                    str_html += f""" <td class="CONTEUDO_PD{DIA_LOGISTICO}">"""  

                    if DADOS_DIA_LOGISTICO["PEDRA"]["P1"] != 0:                    
                        str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P1"])
                        

                    str_html += "</td>" 

                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["SALDOS"]["P2"] != 0:                    
                        str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P2"])
                                
                    
                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""
                        
                    if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P2"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P2"])
                            
                    
                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_PD{DIA_LOGISTICO}">"""     
                        
                    if DADOS_DIA_LOGISTICO["PEDRA"]["P2"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P2"])
                            

                    str_html += "</td>" 
                    
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["SALDOS"]["P3"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P3"])
                            

                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P3"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P3"])
                            

                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_PD{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["PEDRA"]["P3"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P3"])
                            

                    str_html += "</td>" 
                    

                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""
                        
                    if DADOS_DIA_LOGISTICO["SALDOS"]["P4"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P4"])
                            

                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P4"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P4"])
                            
                    
                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_PD{DIA_LOGISTICO}">"""
                        
                    if DADOS_DIA_LOGISTICO["PEDRA"]["P4"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P4"])
                            
                    
                    str_html += "</td>" 
                    
                    
                    str_html += f""" <td class="COLUNA_TOTAL">"""

                    if DADOS_DIA_LOGISTICO["TT_OF"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["TT_OF"])
                            

                    str_html += "</td>"  
                    str_html += f""" <td class="COLUNA_TOTAL">"""

                    if DADOS_DIA_LOGISTICO["TT_PD"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["TT_PD"])
                            

                    str_html += "</td>" 
                
            str_html += "</tr>"      
    #endregion

   #region RELATORIO VLI GRAO PCZ

    if "VLI" in detailed_report:
        
        if detailed_report["VLI"]["GRAOS"]["PCZ"]:
    
            str_html += "<tr>"

            str_html += f""" <th colspan="4" class="NOME__TERMINAL">VLI GRÃO PCZ</th>"""

            for DIA_LOGISTICO, DADOS_DIA_LOGISTICO in  detailed_report["VLI"]["GRAOS"]["PCZ"].items():

                if DIA_LOGISTICO == dia_logistico:

                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["SALDOS"]["P1"] != 0:                    
                        str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P1"]) 
                    

                    str_html += "</td>"   
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P1"] != 0:                    
                        str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P1"])
                        

                    str_html += "</td>"   
                    str_html += f""" <td class="CONTEUDO_PD{DIA_LOGISTICO}">"""  

                    if DADOS_DIA_LOGISTICO["PEDRA"]["P1"] != 0:                    
                        str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P1"])
                        

                    str_html += "</td>" 

                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["SALDOS"]["P2"] != 0:                    
                        str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P2"])
                                
                    
                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""
                        
                    if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P2"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P2"])
                            
                    
                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_PD{DIA_LOGISTICO}">"""     
                        
                    if DADOS_DIA_LOGISTICO["PEDRA"]["P2"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P2"])
                            

                    str_html += "</td>" 
                    
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["SALDOS"]["P3"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P3"])
                            

                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P3"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P3"])
                            

                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_PD{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["PEDRA"]["P3"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P3"])
                            

                    str_html += "</td>" 
                    

                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""
                        
                    if DADOS_DIA_LOGISTICO["SALDOS"]["P4"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P4"])
                            

                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P4"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P4"])
                            
                    
                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_PD{DIA_LOGISTICO}">"""
                        
                    if DADOS_DIA_LOGISTICO["PEDRA"]["P4"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P4"])
                            
                    
                    str_html += "</td>" 
                    
                    
                    str_html += f""" <td class="COLUNA_TOTAL">"""

                    if DADOS_DIA_LOGISTICO["TT_OF"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["TT_OF"])
                            

                    str_html += "</td>"  
                    str_html += f""" <td class="COLUNA_TOTAL">"""

                    if DADOS_DIA_LOGISTICO["TT_PD"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["TT_PD"])
                            

                    str_html += "</td>" 
                
            str_html += "</tr>"      
    #endregion

    #region RELATORIO VLI ACUCAR PSN

    if "VLI" in detailed_report:
        
        if detailed_report["VLI"]["ACUCAR"]["PSN"]:
    
            str_html += "<tr>"

            str_html += f""" <th colspan="4" class="NOME__TERMINAL">VLI AÇÚCAR PSN</th>"""

            for DIA_LOGISTICO, DADOS_DIA_LOGISTICO in  detailed_report["VLI"]["ACUCAR"]["PSN"].items():

                if DIA_LOGISTICO == dia_logistico:

                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["SALDOS"]["P1"] != 0:                    
                        str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P1"]) 
                    

                    str_html += "</td>"   
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P1"] != 0:                    
                        str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P1"])
                        

                    str_html += "</td>"   
                    str_html += f""" <td class="CONTEUDO_PD{DIA_LOGISTICO}">"""  

                    if DADOS_DIA_LOGISTICO["PEDRA"]["P1"] != 0:                    
                        str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P1"])
                        

                    str_html += "</td>" 

                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["SALDOS"]["P2"] != 0:                    
                        str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P2"])
                                
                    
                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""
                        
                    if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P2"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P2"])
                            
                    
                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_PD{DIA_LOGISTICO}">"""     
                        
                    if DADOS_DIA_LOGISTICO["PEDRA"]["P2"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P2"])
                            

                    str_html += "</td>" 
                    
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["SALDOS"]["P3"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P3"])
                            

                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P3"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P3"])
                            

                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_PD{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["PEDRA"]["P3"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P3"])
                            

                    str_html += "</td>" 
                    

                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""
                        
                    if DADOS_DIA_LOGISTICO["SALDOS"]["P4"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P4"])
                            

                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P4"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P4"])
                            
                    
                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_PD{DIA_LOGISTICO}">"""
                        
                    if DADOS_DIA_LOGISTICO["PEDRA"]["P4"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P4"])
                            
                    
                    str_html += "</td>" 
                    
                    
                    str_html += f""" <td class="COLUNA_TOTAL">"""

                    if DADOS_DIA_LOGISTICO["TT_OF"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["TT_OF"])
                            

                    str_html += "</td>"  
                    str_html += f""" <td class="COLUNA_TOTAL">"""

                    if DADOS_DIA_LOGISTICO["TT_PD"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["TT_PD"])
                            

                    str_html += "</td>" 
                
            str_html += "</tr>"      
    #endregion

    #region RELATORIO VLI ACUCAR PCZ

    if "VLI" in detailed_report:
        
        if detailed_report["VLI"]["ACUCAR"]["PCZ"]:
    
            str_html += "<tr>"

            str_html += f""" <th colspan="4" class="NOME__TERMINAL">VLI AÇÚCAR PCZ</th>"""

            for DIA_LOGISTICO, DADOS_DIA_LOGISTICO in  detailed_report["VLI"]["ACUCAR"]["PCZ"].items():

                if DIA_LOGISTICO == dia_logistico:

                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["SALDOS"]["P1"] != 0:                    
                        str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P1"]) 
                    

                    str_html += "</td>"   
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P1"] != 0:                    
                        str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P1"])
                        

                    str_html += "</td>"   
                    str_html += f""" <td class="CONTEUDO_PD{DIA_LOGISTICO}">"""  

                    if DADOS_DIA_LOGISTICO["PEDRA"]["P1"] != 0:                    
                        str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P1"])
                        

                    str_html += "</td>" 

                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["SALDOS"]["P2"] != 0:                    
                        str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P2"])
                                
                    
                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""
                        
                    if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P2"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P2"])
                            
                    
                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_PD{DIA_LOGISTICO}">"""     
                        
                    if DADOS_DIA_LOGISTICO["PEDRA"]["P2"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P2"])
                            

                    str_html += "</td>" 
                    
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["SALDOS"]["P3"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P3"])
                            

                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P3"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P3"])
                            

                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_PD{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["PEDRA"]["P3"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P3"])
                            

                    str_html += "</td>" 
                    

                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""
                        
                    if DADOS_DIA_LOGISTICO["SALDOS"]["P4"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P4"])
                            

                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P4"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P4"])
                            
                    
                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_PD{DIA_LOGISTICO}">"""
                        
                    if DADOS_DIA_LOGISTICO["PEDRA"]["P4"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P4"])
                            
                    
                    str_html += "</td>" 
                    
                    
                    str_html += f""" <td class="COLUNA_TOTAL">"""

                    if DADOS_DIA_LOGISTICO["TT_OF"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["TT_OF"])
                            

                    str_html += "</td>"  
                    str_html += f""" <td class="COLUNA_TOTAL">"""

                    if DADOS_DIA_LOGISTICO["TT_PD"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["TT_PD"])
                            

                    str_html += "</td>" 
                
            str_html += "</tr>"      
    #endregion

    #region  RELATORIO VLI TOTAL GRÃO + ACUCAR

    str_html += """<tr class="TOTAL">"""
    str_html += """<th colspan="4" class=" COLUNA_TOTAL NOME__TERMINAL">TOTAL VLI GRÃOS E AÇÚCAR</th>"""

    for DIA_LOGISTICO, DADOS_DIA_LOGISTICO in  detailed_report["VLI"]["TOTAO_GRAO_ACUCAR"].items():
            if DIA_LOGISTICO == dia_logistico:
                str_html += f""" <td class="TOTAL_{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["SALDOS"]["P1"] != 0:                    
                    str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P1"]) 
                        

                str_html += "</td>" 
                str_html += f""" <td class="TOTAL_{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P1"] != 0:                    
                    str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P1"]) 
                    

                str_html += "</td>"  
                str_html += f""" <td class="TOTAL_PD{DIA_LOGISTICO}">  """

                if DADOS_DIA_LOGISTICO["PEDRA"]["P1"] != 0:                    
                    str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P1"]) 
                        

                str_html += "</td>"

                str_html += f""" <td class="TOTAL_{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["SALDOS"]["P2"] != 0:                    
                    str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P2"] )
                            
                    
                str_html += "</td>"
                str_html += f""" <td class="TOTAL_{DIA_LOGISTICO}">"""
                    
                if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P2"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P2"]) 
                            
                    
                str_html += "</td>"
                str_html += f""" <td class="TOTAL_PD{DIA_LOGISTICO}">"""     
                        
                if DADOS_DIA_LOGISTICO["PEDRA"]["P2"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P2"]) 
                        

                str_html += "</td>"
                str_html += f""" <td class="TOTAL_{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["SALDOS"]["P3"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P3"]) 
                        

                str_html += "</td>"
                str_html += f""" <td class="TOTAL_{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P3"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P3"]) 
                        

                str_html += "</td>"
                str_html += f""" <td class="TOTAL_PD{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["PEDRA"]["P3"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P3"]) 
                        

                str_html += "</td>"
                    

                str_html += f""" <td class="TOTAL_{DIA_LOGISTICO}">"""
                        
                if DADOS_DIA_LOGISTICO["SALDOS"]["P4"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P4"]) 
                        

                str_html += "</td>"
                str_html += f""" <td class="TOTAL_{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P4"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P4"]) 
                        
                    
                str_html += "</td>"
                str_html += f""" <td class="TOTAL_PD{DIA_LOGISTICO}">"""
                        
                if DADOS_DIA_LOGISTICO["PEDRA"]["P4"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P4"]) 
                        
                    
                str_html += "</td>"
                    
                    
                str_html += f""" <td class="TOTAL_TOTAL{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["TT_OF"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["TT_OF"])
                        

                str_html += "</td>"
                str_html += f""" <td class="TOTAL_TOTAL{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["TT_PD"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["TT_PD"]) 
                        

                str_html += "</td>"

            str_html += "</tr>"


    #endregion

    #endregion

    str_html += """<tr><td colspan="72" CLASS="PULA_LINHA">.</td></tr>"""

    #region RELATORIO MRS

    #region RELATORIO MRS GRAO PSN

    if "MRS" in detailed_report:
        
        if detailed_report["MRS"]["GRAOS"]["PSN"]:
    
            str_html += "<tr>"

            str_html += f""" <th colspan="4" class="NOME__TERMINAL">MRS GRÃO PSN</th>"""

            for DIA_LOGISTICO, DADOS_DIA_LOGISTICO in  detailed_report["MRS"]["GRAOS"]["PSN"].items():

                if DIA_LOGISTICO == dia_logistico:

                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["SALDOS"]["P1"] != 0:                    
                        str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P1"]) 
                    

                    str_html += "</td>"   
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P1"] != 0:                    
                        str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P1"])
                        

                    str_html += "</td>"   
                    str_html += f""" <td class="CONTEUDO_PD{DIA_LOGISTICO}">"""  

                    if DADOS_DIA_LOGISTICO["PEDRA"]["P1"] != 0:                    
                        str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P1"])
                        

                    str_html += "</td>" 

                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["SALDOS"]["P2"] != 0:                    
                        str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P2"])
                                
                    
                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""
                        
                    if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P2"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P2"])
                            
                    
                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_PD{DIA_LOGISTICO}">"""     
                        
                    if DADOS_DIA_LOGISTICO["PEDRA"]["P2"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P2"])
                            

                    str_html += "</td>" 
                    
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["SALDOS"]["P3"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P3"])
                            

                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P3"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P3"])
                            

                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_PD{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["PEDRA"]["P3"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P3"])
                            

                    str_html += "</td>" 
                    

                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""
                        
                    if DADOS_DIA_LOGISTICO["SALDOS"]["P4"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P4"])
                            

                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P4"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P4"])
                            
                    
                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_PD{DIA_LOGISTICO}">"""
                        
                    if DADOS_DIA_LOGISTICO["PEDRA"]["P4"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P4"])
                            
                    
                    str_html += "</td>" 
                    
                    
                    str_html += f""" <td class="COLUNA_TOTAL">"""

                    if DADOS_DIA_LOGISTICO["TT_OF"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["TT_OF"])
                            

                    str_html += "</td>"  
                    str_html += f""" <td class="COLUNA_TOTAL">"""

                    if DADOS_DIA_LOGISTICO["TT_PD"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["TT_PD"])
                            

                    str_html += "</td>" 
                
            str_html += "</tr>"      
    #endregion    

    #region RELATORIO MRS GRAO PCZ

    if "MRS" in detailed_report:
        
        if detailed_report["MRS"]["GRAOS"]["PCZ"]:
    
            str_html += "<tr>"

            str_html += f""" <th colspan="4" class="NOME__TERMINAL">MRS GRÃO PCZ</th>"""

            for DIA_LOGISTICO, DADOS_DIA_LOGISTICO in  detailed_report["MRS"]["GRAOS"]["PCZ"].items():

                if DIA_LOGISTICO == dia_logistico:

                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["SALDOS"]["P1"] != 0:                    
                        str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P1"]) 
                    

                    str_html += "</td>"   
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P1"] != 0:                    
                        str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P1"])
                        

                    str_html += "</td>"   
                    str_html += f""" <td class="CONTEUDO_PD{DIA_LOGISTICO}">"""  

                    if DADOS_DIA_LOGISTICO["PEDRA"]["P1"] != 0:                    
                        str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P1"])
                        

                    str_html += "</td>" 

                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["SALDOS"]["P2"] != 0:                    
                        str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P2"])
                                
                    
                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""
                        
                    if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P2"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P2"])
                            
                    
                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_PD{DIA_LOGISTICO}">"""     
                        
                    if DADOS_DIA_LOGISTICO["PEDRA"]["P2"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P2"])
                            

                    str_html += "</td>" 
                    
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["SALDOS"]["P3"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P3"])
                            

                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P3"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P3"])
                            

                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_PD{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["PEDRA"]["P3"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P3"])
                            

                    str_html += "</td>" 
                    

                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""
                        
                    if DADOS_DIA_LOGISTICO["SALDOS"]["P4"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P4"])
                            

                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P4"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P4"])
                            
                    
                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_PD{DIA_LOGISTICO}">"""
                        
                    if DADOS_DIA_LOGISTICO["PEDRA"]["P4"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P4"])
                            
                    
                    str_html += "</td>" 
                    
                    
                    str_html += f""" <td class="COLUNA_TOTAL">"""

                    if DADOS_DIA_LOGISTICO["TT_OF"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["TT_OF"])
                            

                    str_html += "</td>"  
                    str_html += f""" <td class="COLUNA_TOTAL">"""

                    if DADOS_DIA_LOGISTICO["TT_PD"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["TT_PD"])
                            

                    str_html += "</td>" 
                
            str_html += "</tr>"      
    #endregion    

    #region RELATORIO MRS ACUCAR PSN

    if "MRS" in detailed_report:
        
        if detailed_report["MRS"]["ACUCAR"]["PSN"]:
    
            str_html += "<tr>"

            str_html += f""" <th colspan="4" class="NOME__TERMINAL">MRS AÇÚCAR PSN</th>"""

            for DIA_LOGISTICO, DADOS_DIA_LOGISTICO in  detailed_report["MRS"]["ACUCAR"]["PSN"].items():

                if DIA_LOGISTICO == dia_logistico:

                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["SALDOS"]["P1"] != 0:                    
                        str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P1"]) 
                    

                    str_html += "</td>"   
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P1"] != 0:                    
                        str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P1"])
                        

                    str_html += "</td>"   
                    str_html += f""" <td class="CONTEUDO_PD{DIA_LOGISTICO}">"""  

                    if DADOS_DIA_LOGISTICO["PEDRA"]["P1"] != 0:                    
                        str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P1"])
                        

                    str_html += "</td>" 

                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["SALDOS"]["P2"] != 0:                    
                        str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P2"])
                                
                    
                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""
                        
                    if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P2"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P2"])
                            
                    
                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_PD{DIA_LOGISTICO}">"""     
                        
                    if DADOS_DIA_LOGISTICO["PEDRA"]["P2"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P2"])
                            

                    str_html += "</td>" 
                    
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["SALDOS"]["P3"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P3"])
                            

                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P3"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P3"])
                            

                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_PD{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["PEDRA"]["P3"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P3"])
                            

                    str_html += "</td>" 
                    

                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""
                        
                    if DADOS_DIA_LOGISTICO["SALDOS"]["P4"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P4"])
                            

                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P4"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P4"])
                            
                    
                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_PD{DIA_LOGISTICO}">"""
                        
                    if DADOS_DIA_LOGISTICO["PEDRA"]["P4"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P4"])
                            
                    
                    str_html += "</td>" 
                    
                    
                    str_html += f""" <td class="COLUNA_TOTAL">"""

                    if DADOS_DIA_LOGISTICO["TT_OF"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["TT_OF"])
                            

                    str_html += "</td>"  
                    str_html += f""" <td class="COLUNA_TOTAL">"""

                    if DADOS_DIA_LOGISTICO["TT_PD"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["TT_PD"])
                            

                    str_html += "</td>" 
                
            str_html += "</tr>"      
    #endregion    

    #region RELATORIO MRS ACUCAR PCZ

    if "MRS" in detailed_report:
        
        if detailed_report["MRS"]["ACUCAR"]["PCZ"]:
    
            str_html += "<tr>"

            str_html += f""" <th colspan="4" class="NOME__TERMINAL">MRS AÇÚCAR PCZ</th>"""

            for DIA_LOGISTICO, DADOS_DIA_LOGISTICO in  detailed_report["MRS"]["ACUCAR"]["PCZ"].items():

                if DIA_LOGISTICO == dia_logistico:

                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["SALDOS"]["P1"] != 0:                    
                        str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P1"]) 
                    

                    str_html += "</td>"   
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P1"] != 0:                    
                        str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P1"])
                        

                    str_html += "</td>"   
                    str_html += f""" <td class="CONTEUDO_PD{DIA_LOGISTICO}">"""  

                    if DADOS_DIA_LOGISTICO["PEDRA"]["P1"] != 0:                    
                        str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P1"])
                        

                    str_html += "</td>" 

                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["SALDOS"]["P2"] != 0:                    
                        str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P2"])
                                
                    
                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""
                        
                    if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P2"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P2"])
                            
                    
                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_PD{DIA_LOGISTICO}">"""     
                        
                    if DADOS_DIA_LOGISTICO["PEDRA"]["P2"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P2"])
                            

                    str_html += "</td>" 
                    
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["SALDOS"]["P3"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P3"])
                            

                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P3"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P3"])
                            

                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_PD{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["PEDRA"]["P3"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P3"])
                            

                    str_html += "</td>" 
                    

                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""
                        
                    if DADOS_DIA_LOGISTICO["SALDOS"]["P4"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P4"])
                            

                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P4"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P4"])
                            
                    
                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_PD{DIA_LOGISTICO}">"""
                        
                    if DADOS_DIA_LOGISTICO["PEDRA"]["P4"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P4"])
                            
                    
                    str_html += "</td>" 
                    
                    
                    str_html += f""" <td class="COLUNA_TOTAL">"""

                    if DADOS_DIA_LOGISTICO["TT_OF"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["TT_OF"])
                            

                    str_html += "</td>"  
                    str_html += f""" <td class="COLUNA_TOTAL">"""

                    if DADOS_DIA_LOGISTICO["TT_PD"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["TT_PD"])
                            

                    str_html += "</td>" 
                
            str_html += "</tr>"      
    #endregion   

    #region RELATORIO MRS TOTAL GRÃO + ACUCAR

    str_html += """<tr class="TOTAL">"""
    str_html += """<th colspan="4" class=" COLUNA_TOTAL NOME__TERMINAL">TOTAL MRS GRÃOS E AÇÚCAR</th>"""

    for DIA_LOGISTICO, DADOS_DIA_LOGISTICO in  detailed_report["MRS"]["TOTAO_GRAO_ACUCAR"].items():
            if DIA_LOGISTICO == dia_logistico:
                str_html += f""" <td class="TOTAL_{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["SALDOS"]["P1"] != 0:                    
                    str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P1"]) 
                        

                str_html += "</td>" 
                str_html += f""" <td class="TOTAL_{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P1"] != 0:                    
                    str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P1"]) 
                    

                str_html += "</td>"  
                str_html += f""" <td class="TOTAL_PD{DIA_LOGISTICO}">  """

                if DADOS_DIA_LOGISTICO["PEDRA"]["P1"] != 0:                    
                    str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P1"]) 
                        

                str_html += "</td>"

                str_html += f""" <td class="TOTAL_{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["SALDOS"]["P2"] != 0:                    
                    str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P2"] )
                            
                    
                str_html += "</td>"
                str_html += f""" <td class="TOTAL_{DIA_LOGISTICO}">"""
                    
                if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P2"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P2"]) 
                            
                    
                str_html += "</td>"
                str_html += f""" <td class="TOTAL_PD{DIA_LOGISTICO}">"""     
                        
                if DADOS_DIA_LOGISTICO["PEDRA"]["P2"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P2"]) 
                        

                str_html += "</td>"
                str_html += f""" <td class="TOTAL_{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["SALDOS"]["P3"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P3"]) 
                        

                str_html += "</td>"
                str_html += f""" <td class="TOTAL_{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P3"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P3"]) 
                        

                str_html += "</td>"
                str_html += f""" <td class="TOTAL_PD{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["PEDRA"]["P3"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P3"]) 
                        

                str_html += "</td>"
                    

                str_html += f""" <td class="TOTAL_{DIA_LOGISTICO}">"""
                        
                if DADOS_DIA_LOGISTICO["SALDOS"]["P4"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P4"]) 
                        

                str_html += "</td>"
                str_html += f""" <td class="TOTAL_{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P4"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P4"]) 
                        
                    
                str_html += "</td>"
                str_html += f""" <td class="TOTAL_PD{DIA_LOGISTICO}">"""
                        
                if DADOS_DIA_LOGISTICO["PEDRA"]["P4"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P4"]) 
                        
                    
                str_html += "</td>"
                    
                    
                str_html += f""" <td class="TOTAL_TOTAL{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["TT_OF"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["TT_OF"])
                        

                str_html += "</td>"
                str_html += f""" <td class="TOTAL_TOTAL{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["TT_PD"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["TT_PD"]) 
                        

                str_html += "</td>"

            str_html += "</tr>"


    #endregion

    #region RELATORIO MRS CELULOSE PSN

    if "MRS" in detailed_report:
        
        if detailed_report["MRS"]["CELULOSE"]["PSN"]:
    
            str_html += "<tr>"

            str_html += f""" <th colspan="4" class="NOME__TERMINAL">MRS CELULOSE PSN</th>"""

            for DIA_LOGISTICO, DADOS_DIA_LOGISTICO in  detailed_report["MRS"]["CELULOSE"]["PSN"].items():

                if DIA_LOGISTICO == dia_logistico:

                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["SALDOS"]["P1"] != 0:                    
                        str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P1"]) 
                    

                    str_html += "</td>"   
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P1"] != 0:                    
                        str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P1"])
                        

                    str_html += "</td>"   
                    str_html += f""" <td class="CONTEUDO_PD{DIA_LOGISTICO}">"""  

                    if DADOS_DIA_LOGISTICO["PEDRA"]["P1"] != 0:                    
                        str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P1"])
                        

                    str_html += "</td>" 

                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["SALDOS"]["P2"] != 0:                    
                        str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P2"])
                                
                    
                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""
                        
                    if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P2"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P2"])
                            
                    
                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_PD{DIA_LOGISTICO}">"""     
                        
                    if DADOS_DIA_LOGISTICO["PEDRA"]["P2"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P2"])
                            

                    str_html += "</td>" 
                    
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["SALDOS"]["P3"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P3"])
                            

                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P3"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P3"])
                            

                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_PD{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["PEDRA"]["P3"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P3"])
                            

                    str_html += "</td>" 
                    

                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""
                        
                    if DADOS_DIA_LOGISTICO["SALDOS"]["P4"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P4"])
                            

                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P4"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P4"])
                            
                    
                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_PD{DIA_LOGISTICO}">"""
                        
                    if DADOS_DIA_LOGISTICO["PEDRA"]["P4"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P4"])
                            
                    
                    str_html += "</td>" 
                    
                    
                    str_html += f""" <td class="COLUNA_TOTAL">"""

                    if DADOS_DIA_LOGISTICO["TT_OF"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["TT_OF"])
                            

                    str_html += "</td>"  
                    str_html += f""" <td class="COLUNA_TOTAL">"""

                    if DADOS_DIA_LOGISTICO["TT_PD"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["TT_PD"])
                            

                    str_html += "</td>" 
                
            str_html += "</tr>"      
    #endregion 

    #region RELATORIO MRS TOTAL CELULOSE

    str_html += """<tr class="TOTAL">"""
    str_html += """<th colspan="4" class=" COLUNA_TOTAL NOME__TERMINAL">TOTAL MRS CELULOSE</th>"""

    for DIA_LOGISTICO, DADOS_DIA_LOGISTICO in  detailed_report["MRS"]["CELULOSE"]["TOTAL_CELULOSE"].items():
            if DIA_LOGISTICO == dia_logistico:
                str_html += f""" <td class="TOTAL_{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["SALDOS"]["P1"] != 0:                    
                    str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P1"]) 
                        

                str_html += "</td>" 
                str_html += f""" <td class="TOTAL_{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P1"] != 0:                    
                    str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P1"]) 
                    

                str_html += "</td>"  
                str_html += f""" <td class="TOTAL_PD{DIA_LOGISTICO}">  """

                if DADOS_DIA_LOGISTICO["PEDRA"]["P1"] != 0:                    
                    str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P1"]) 
                        

                str_html += "</td>"

                str_html += f""" <td class="TOTAL_{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["SALDOS"]["P2"] != 0:                    
                    str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P2"] )
                            
                    
                str_html += "</td>"
                str_html += f""" <td class="TOTAL_{DIA_LOGISTICO}">"""
                    
                if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P2"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P2"]) 
                            
                    
                str_html += "</td>"
                str_html += f""" <td class="TOTAL_PD{DIA_LOGISTICO}">"""     
                        
                if DADOS_DIA_LOGISTICO["PEDRA"]["P2"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P2"]) 
                        

                str_html += "</td>"
                str_html += f""" <td class="TOTAL_{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["SALDOS"]["P3"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P3"]) 
                        

                str_html += "</td>"
                str_html += f""" <td class="TOTAL_{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P3"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P3"]) 
                        

                str_html += "</td>"
                str_html += f""" <td class="TOTAL_PD{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["PEDRA"]["P3"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P3"]) 
                        

                str_html += "</td>"
                    

                str_html += f""" <td class="TOTAL_{DIA_LOGISTICO}">"""
                        
                if DADOS_DIA_LOGISTICO["SALDOS"]["P4"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P4"]) 
                        

                str_html += "</td>"
                str_html += f""" <td class="TOTAL_{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P4"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P4"]) 
                        
                    
                str_html += "</td>"
                str_html += f""" <td class="TOTAL_PD{DIA_LOGISTICO}">"""
                        
                if DADOS_DIA_LOGISTICO["PEDRA"]["P4"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P4"]) 
                        
                    
                str_html += "</td>"
                    
                    
                str_html += f""" <td class="TOTAL_TOTAL{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["TT_OF"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["TT_OF"])
                        

                str_html += "</td>"
                str_html += f""" <td class="TOTAL_TOTAL{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["TT_PD"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["TT_PD"]) 
                        

                str_html += "</td>"

            str_html += "</tr>"


    #endregion

    #region RELATORIO MRS CONTEINER PSN

    if "MRS" in detailed_report:
        
        if detailed_report["MRS"]["CONTEINER"]["PSN"]:
    
            str_html += "<tr>"

            str_html += f""" <th colspan="4" class="NOME__TERMINAL">MRS CONTEINER PSN</th>"""

            for DIA_LOGISTICO, DADOS_DIA_LOGISTICO in  detailed_report["MRS"]["CONTEINER"]["PSN"].items():

                if DIA_LOGISTICO == dia_logistico:

                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["SALDOS"]["P1"] != 0:                    
                        str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P1"]) 
                    

                    str_html += "</td>"   
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P1"] != 0:                    
                        str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P1"])
                        

                    str_html += "</td>"   
                    str_html += f""" <td class="CONTEUDO_PD{DIA_LOGISTICO}">"""  

                    if DADOS_DIA_LOGISTICO["PEDRA"]["P1"] != 0:                    
                        str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P1"])
                        

                    str_html += "</td>" 

                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["SALDOS"]["P2"] != 0:                    
                        str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P2"])
                                
                    
                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""
                        
                    if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P2"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P2"])
                            
                    
                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_PD{DIA_LOGISTICO}">"""     
                        
                    if DADOS_DIA_LOGISTICO["PEDRA"]["P2"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P2"])
                            

                    str_html += "</td>" 
                    
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["SALDOS"]["P3"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P3"])
                            

                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P3"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P3"])
                            

                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_PD{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["PEDRA"]["P3"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P3"])
                            

                    str_html += "</td>" 
                    

                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""
                        
                    if DADOS_DIA_LOGISTICO["SALDOS"]["P4"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P4"])
                            

                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P4"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P4"])
                            
                    
                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_PD{DIA_LOGISTICO}">"""
                        
                    if DADOS_DIA_LOGISTICO["PEDRA"]["P4"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P4"])
                            
                    
                    str_html += "</td>" 
                    
                    
                    str_html += f""" <td class="COLUNA_TOTAL">"""

                    if DADOS_DIA_LOGISTICO["TT_OF"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["TT_OF"])
                            

                    str_html += "</td>"  
                    str_html += f""" <td class="COLUNA_TOTAL">"""

                    if DADOS_DIA_LOGISTICO["TT_PD"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["TT_PD"])
                            

                    str_html += "</td>" 
                
            str_html += "</tr>"      
    #endregion 

    #region RELATORIO MRS CONTEINER PCZ

    if "MRS" in detailed_report:
        
        if detailed_report["MRS"]["CONTEINER"]["PCZ"]:
    
            str_html += "<tr>"

            str_html += f""" <th colspan="4" class="NOME__TERMINAL">MRS CONTEINER PCZ</th>"""

            for DIA_LOGISTICO, DADOS_DIA_LOGISTICO in  detailed_report["MRS"]["CONTEINER"]["PCZ"].items():

                if DIA_LOGISTICO == dia_logistico:

                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["SALDOS"]["P1"] != 0:                    
                        str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P1"]) 
                    

                    str_html += "</td>"   
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P1"] != 0:                    
                        str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P1"])
                        

                    str_html += "</td>"   
                    str_html += f""" <td class="CONTEUDO_PD{DIA_LOGISTICO}">"""  

                    if DADOS_DIA_LOGISTICO["PEDRA"]["P1"] != 0:                    
                        str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P1"])
                        

                    str_html += "</td>" 

                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["SALDOS"]["P2"] != 0:                    
                        str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P2"])
                                
                    
                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""
                        
                    if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P2"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P2"])
                            
                    
                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_PD{DIA_LOGISTICO}">"""     
                        
                    if DADOS_DIA_LOGISTICO["PEDRA"]["P2"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P2"])
                            

                    str_html += "</td>" 
                    
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["SALDOS"]["P3"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P3"])
                            

                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P3"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P3"])
                            

                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_PD{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["PEDRA"]["P3"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P3"])
                            

                    str_html += "</td>" 
                    

                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""
                        
                    if DADOS_DIA_LOGISTICO["SALDOS"]["P4"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P4"])
                            

                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_{DIA_LOGISTICO}">"""

                    if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P4"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P4"])
                            
                    
                    str_html += "</td>" 
                    str_html += f""" <td class="CONTEUDO_PD{DIA_LOGISTICO}">"""
                        
                    if DADOS_DIA_LOGISTICO["PEDRA"]["P4"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P4"])
                            
                    
                    str_html += "</td>" 
                    
                    
                    str_html += f""" <td class="COLUNA_TOTAL">"""

                    if DADOS_DIA_LOGISTICO["TT_OF"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["TT_OF"])
                            

                    str_html += "</td>"  
                    str_html += f""" <td class="COLUNA_TOTAL">"""

                    if DADOS_DIA_LOGISTICO["TT_PD"] != 0:                      
                        str_html +=   str(DADOS_DIA_LOGISTICO["TT_PD"])
                            

                    str_html += "</td>" 
                
            str_html += "</tr>"      
    #endregion 

    #region RELATORIO MRS TOTAL CONTEINER

    str_html += """<tr class="TOTAL">"""
    str_html += """<th colspan="4" class=" COLUNA_TOTAL NOME__TERMINAL">TOTAL MRS GRÃOS E AÇÚCAR</th>"""

    for DIA_LOGISTICO, DADOS_DIA_LOGISTICO in  detailed_report["MRS"]["CONTEINER"]["TOTAL_CONTEINER"].items():
            if DIA_LOGISTICO == dia_logistico:
                str_html += f""" <td class="TOTAL_{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["SALDOS"]["P1"] != 0:                    
                    str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P1"]) 
                        

                str_html += "</td>" 
                str_html += f""" <td class="TOTAL_{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P1"] != 0:                    
                    str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P1"]) 
                    

                str_html += "</td>"  
                str_html += f""" <td class="TOTAL_PD{DIA_LOGISTICO}">  """

                if DADOS_DIA_LOGISTICO["PEDRA"]["P1"] != 0:                    
                    str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P1"]) 
                        

                str_html += "</td>"

                str_html += f""" <td class="TOTAL_{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["SALDOS"]["P2"] != 0:                    
                    str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P2"] )
                            
                    
                str_html += "</td>"
                str_html += f""" <td class="TOTAL_{DIA_LOGISTICO}">"""
                    
                if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P2"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P2"]) 
                            
                    
                str_html += "</td>"
                str_html += f""" <td class="TOTAL_PD{DIA_LOGISTICO}">"""     
                        
                if DADOS_DIA_LOGISTICO["PEDRA"]["P2"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P2"]) 
                        

                str_html += "</td>"
                str_html += f""" <td class="TOTAL_{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["SALDOS"]["P3"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P3"]) 
                        

                str_html += "</td>"
                str_html += f""" <td class="TOTAL_{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P3"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P3"]) 
                        

                str_html += "</td>"
                str_html += f""" <td class="TOTAL_PD{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["PEDRA"]["P3"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P3"]) 
                        

                str_html += "</td>"
                    

                str_html += f""" <td class="TOTAL_{DIA_LOGISTICO}">"""
                        
                if DADOS_DIA_LOGISTICO["SALDOS"]["P4"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["SALDOS"]["P4"]) 
                        

                str_html += "</td>"
                str_html += f""" <td class="TOTAL_{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P4"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["RECEBIMENTOS"]["P4"]) 
                        
                    
                str_html += "</td>"
                str_html += f""" <td class="TOTAL_PD{DIA_LOGISTICO}">"""
                        
                if DADOS_DIA_LOGISTICO["PEDRA"]["P4"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["PEDRA"]["P4"]) 
                        
                    
                str_html += "</td>"
                    
                    
                str_html += f""" <td class="TOTAL_TOTAL{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["TT_OF"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["TT_OF"])
                        

                str_html += "</td>"
                str_html += f""" <td class="TOTAL_TOTAL{DIA_LOGISTICO}">"""

                if DADOS_DIA_LOGISTICO["TT_PD"] != 0:                      
                    str_html +=   str(DADOS_DIA_LOGISTICO["TT_PD"]) 
                        

                str_html += "</td>"

            str_html += "</tr>"


    #endregion

    #endregion

    str_html += """<tr><td colspan="72" CLASS="PULA_LINHA">.</td></tr>"""

    #region TOTAIS FIPS


    #endregion

    html_detalhe = table_header + str_html + " </table>"
    html_detalhe = "<html><head><style>" + css_style + "</style></head><body style='padding: 20px'> " + html_detalhe +  "</body></html>" 

    return html_detalhe