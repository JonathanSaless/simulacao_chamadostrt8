import simpy as sp

class Chamado:
    def __init__(self, env, id_chamado, t_chegada, t_resolucao, dps_resolucao, registro, central_manha, central_tarde, eqp_de_campo_manha, eqp_de_campo_tarde, sv_infra):
        self.env = env
        self.id_chamado = id_chamado
        self.t_chegada = t_chegada
        self.t_resolucao = t_resolucao
        self.central_manha = central_manha
        self.central_tarde = central_tarde
        self.eqp_de_campo_manha = eqp_de_campo_manha
        self.eqp_de_campo_tarde = eqp_de_campo_tarde
        self.sv_infra = sv_infra
        self.dps_resolucao = dps_resolucao
        self.registro = registro
        
        self.env.process(self.chegada_do_chamado())
        
    def chegada_do_chamado(self):
        yield self.env.timeout(int(self.t_chegada))
        print(f"📢{self.id_chamado:<6} chegou às {self.registro}. [Tempo: {self.env.now}]")
        self.env.process(self.atendimento_central())
              
    def atendimento_central(self):
        if ((int(self.registro[0]+self.registro[1])>=12) and (int(self.registro[0]+self.registro[1])<16)):
            with self.central_tarde.request() as central:
                yield central
                print(f"⌨{self.id_chamado:<6} começa atendimento pela CENTRAL. [Tempo: {self.env.now}]")
                if (self.dps_resolucao == "GR CENTRAL"):                
                    yield self.env.timeout(int(self.t_resolucao))
                    print(f"✅{self.id_chamado:<6} resolvido pela CENTRAL. [Tempo: {self.env.now}]")
                elif (self.dps_resolucao == "GR EQUIPE DE CAMPO"):
                    yield self.env.timeout(5)                           #tempo estipulado com base no que vi nos chamados, geralmente leva de 3 a 5 minutos para um chamado ser reencaminhado para a equipe competente
                    print(f"🤝{self.id_chamado:<6} CENTRAL encaminha para EQUIPE DE CAMPO. [Tempo: {self.env.now}]")
                    self.env.process(self.atendimento_eqp_campo())
                elif (self.dps_resolucao == "GR SV INFRA"):
                    yield self.env.timeout(5)
                    print(f"🤝{self.id_chamado:<6} CENTRAL encaminha para SERVICOS INFRA. [Tempo: {self.env.now}]")
                    self.env.process(self.atendimento_sv_infra())

        else:
            with self.central_manha.request() as central:
                yield central
                print(f"⌨{self.id_chamado:<6} começa atendimento pela CENTRAL. [Tempo: {self.env.now}]")
                if (self.dps_resolucao == "GR CENTRAL"):                
                    yield self.env.timeout(int(self.t_resolucao))
                    print(f"✅{self.id_chamado:<6} resolvido pela CENTRAL. [Tempo: {self.env.now}]")
                elif (self.dps_resolucao == "GR EQUIPE DE CAMPO"):
                    yield self.env.timeout(5)                           #tempo estipulado com base no que vi nos chamados, geralmente leva de 3 a 5 minutos para um chamado ser reencaminhado para a equipe competente
                    print(f"🤝{self.id_chamado:<6} CENTRAL encaminha para EQUIPE DE CAMPO. [Tempo: {self.env.now}]")
                    self.env.process(self.atendimento_eqp_campo())
                elif (self.dps_resolucao == "GR SV INFRA"):
                    yield self.env.timeout(5)
                    print(f"🤝{self.id_chamado:<6} CENTRAL encaminha para SERVICOS INFRA. [Tempo: {self.env.now}]")
                    self.env.process(self.atendimento_sv_infra())    
    
    def atendimento_eqp_campo(self):
        if ((int(self.registro[0]+self.registro[1])>=12) and (int(self.registro[0]+self.registro[1])<16)):
            with self.eqp_de_campo_tarde.request() as equipe_de_campo:
                yield equipe_de_campo
                print(f"⌨{self.id_chamado:<6} começa atendimento pela EQUIPE DE CAMPO. [Tempo: {self.env.now}]")
                yield self.env.timeout(int(self.t_resolucao))
                print(f"✅{self.id_chamado:<6} resolvido pela EQUIPE DE CAMPO. [Tempo: {self.env.now}]")
        else:
            with self.eqp_de_campo_manha.request() as equipe_de_campo:
                yield equipe_de_campo
                print(f"⌨{self.id_chamado:<6} começa atendimento pela EQUIPE DE CAMPO. [Tempo: {self.env.now}]")
                yield self.env.timeout(int(self.t_resolucao))
                print(f"✅{self.id_chamado:<6} resolvido pela EQUIPE DE CAMPO. [Tempo: {self.env.now}]")
                   
    def atendimento_sv_infra(self):
        with self.sv_infra.request() as sv_infra:
            yield sv_infra
            print(f"⌨{self.id_chamado:<6} começa atendimento pelo SERVIÇOS INFRA. [Tempo: {self.env.now}]")
            yield self.env.timeout(int(self.t_resolucao))
            print(f"✅{self.id_chamado:<6} resolvido pelo SERVIÇOS INFRA. [Tempo: {self.env.now}]")