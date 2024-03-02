# ContaEmDia

## Objetivos do Sistema

O Sistema deve permitir controle adequado das finanças do usuário por meio do controle de contas Pagar/Receber e Saldos diversos atualizados seguindo regime de caixa.  

- Login/Logout
- Adicionar Transação Financeira (Despesa/Receita)
- Adicionar parcelamento
- Adicionar e manter atualizados saldos
- Ignorar compras com crédito na contagem de saldo (pois esses só terão efeito de caixa no pagamento da fatura)
- Deve poder associar um lançamento a um centro de Despesas/Receitas

## Lista de Eventos
- [ ] Login de Usuário
- [ ] Lançamento de Transações (Receita/Despesa)
- [ ] Cadastro de Categorias
- [ ] Cadastro de Contas
- [ ] Requisição de Relatorio de Contas
- [ ] Requisição de Relatórios de Transações (Pendentes/Liquidadas)
- [ ] Simulação de Fluxo de Caixa	
- [ ] Tranferir Saldos Entre Contas	



## Opcionais:
    - Deve oferecer opção de não pagar em finais de semana
    - Deve Oferecer opções para aplicação de recursos sempre que houver saldo parado em contas
    - Deve oferecer um mapa de troca entre Contas para melhor alocação de recursos
    



Referências:
 - https://lewoudar.medium.com/fastapi-and-pagination-d27ad52983a
 - https://uriyyo-fastapi-pagination.netlify.app/tutorials/first-steps/
 - https://github.com/DerevenetsArtyom/ultimate-fastapi-tutorial
 - https://christophergs.com/tutorials/ultimate-fastapi-tutorial-pt-11-dependency-injection/
 - https://github.com/LTMullineux/fastapi-snippets/tree/main/00-ultimate-fastapi-project-setup
 - https://medium.com/@lawsontaylor/the-ultimate-fastapi-project-setup-fastapi-async-postgres-sqlmodel-pytest-and-docker-ed0c6afea11b