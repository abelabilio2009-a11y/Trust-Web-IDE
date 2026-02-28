import sys
import random

def processar_logica(linhas, variaveis, funcoes=None):
    if funcoes is None: funcoes = {}
    saida = []
    i = 0
    while i < len(linhas):
        linha = linhas[i].strip()
        
        if not linha or linha.startswith("//"):
            i += 1
            continue

        try:
            # --- COMANDO: FUNC (Declaração de Função) ---
            if linha.startswith("func "):
                nome_func = linha[5:linha.find("(")].strip()
                corpo_func = []
                j = i + 1
                while j < len(linhas) and "};" not in linhas[j]:
                    corpo_func.append(linhas[j]); j += 1
                funcoes[nome_func] = corpo_func
                i = j

            # --- COMANDO: PRINT ---
            elif linha.startswith("print("):
                conteudo = linha[6:-1].replace('"', '').strip()
                resultado = str(variaveis.get(conteudo, conteudo))
                saida.append(resultado)

            # --- COMANDO: LET (Variaveis, Random e Matemática) ---
            elif linha.startswith("let "):
                declaracao = linha[4:].replace(";", "")
                nome_var, valor_raw = [x.strip() for x in declaracao.split("=")]
                
                if "random(" in valor_raw:
                    params = valor_raw[valor_raw.find("(")+1 : valor_raw.find(")")].split(",")
                    variaveis[nome_var] = str(random.randint(int(params[0]), int(params[1])))
                elif "[" in valor_raw:
                    valor_limpo = valor_raw.replace("[", "").replace("]", "").replace('"', '')
                    variaveis[nome_var] = [item.strip() for item in valor_limpo.split(",")]
                elif any(op in valor_raw for op in ["+", "-", "*", "/"]):
                    expressao = valor_raw
                    for var, val in variaveis.items():
                        if isinstance(val, str) and val.isdigit():
                            expressao = expressao.replace(var, val)
                    variaveis[nome_var] = str(eval(expressao))
                else:
                    variaveis[nome_var] = valor_raw.replace('"', '')

            # --- CHAMADA DE FUNÇÃO (ex: atacar()) ---
            elif "()" in linha and not linha.startswith("if"):
                nome_chamada = linha.replace("()", "").replace(";", "").strip()
                if nome_chamada in funcoes:
                    resultado_func = processar_logica(funcoes[nome_chamada], variaveis, funcoes)
                    saida.extend(resultado_func)
                else:
                    saida.append(f"[ERRO] Função '{nome_chamada}' não definida.")

            # --- COMANDO: IF ---
            elif linha.startswith("if"):
                condicao = linha[linha.find("(")+1 : linha.find(")")]
                partes = condicao.split(" ")
                var_nome, operador, valor_comp = partes[0], partes[1], partes[2].replace('"', '')
                valor_atual = variaveis.get(var_nome, "0")
                
                val1 = int(valor_atual) if str(valor_atual).isdigit() else valor_atual
                val2 = int(valor_comp) if str(valor_comp).isdigit() else valor_comp
                
                sucesso = False
                if operador == "==": sucesso = val1 == val2
                elif operador == ">": sucesso = val1 > val2
                elif operador == "<": sucesso = val1 < val2
                
                corpo_if = []
                j = i + 1
                while j < len(linhas) and "};" not in linhas[j]:
                    corpo_if.append(linhas[j]); j += 1
                if sucesso:
                    saida.extend(processar_logica(corpo_if, variaveis, funcoes))
                i = j 

            else:
                saida.append(f"[ERRO DE SINTAXE] Linha {i+1}: Comando '{linha}' não reconhecido.")

        except Exception as e:
            saida.append(f"[ERRO FATAL] Linha {i+1}: {str(e)}")

        i += 1
    return saida

def executar_trust_web(codigo):
    linhas = [l.strip() for l in codigo.split('\n') if l.strip()]
    return processar_logica(linhas, {})