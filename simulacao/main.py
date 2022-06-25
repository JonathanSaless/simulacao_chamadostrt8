import simpy as sp
import csv
import chamados as c
    
if __name__ == "__main__":  
    env = sp.Environment()
    atendentes_central_manha = sp.Resource(env, capacity = 9)
    atendentes_central_tarde = sp.Resource(env, capacity = 7)
    atendentes_eqp_campo_manha = sp.Resource(env, capacity = 9)
    atendentes_eqp_campo_tarde = sp.Resource(env, capacity = 4)
    atendentes_sv_infra = sp.Resource(env, capacity = 3)

    arquivo = open("chamados.csv")
    chamados = csv.DictReader(arquivo)

    for chamado in chamados:
        atendimento = c.Chamado(env, chamado["id"], chamado["tempo_de_chegada"], chamado["tempo_de_resolucao"], chamado["DPS_resolucao"], chamado["hora_registro"], atendentes_central_manha, atendentes_central_tarde, atendentes_eqp_campo_manha, atendentes_eqp_campo_tarde, atendentes_sv_infra)
    
    env.run()