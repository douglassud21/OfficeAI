const form = document.getElementById('form-solicitacao');
const textarea = document.getElementById('texto_original');
const btnEnviar = document.getElementById('btn-enviar');
const feedback = document.getElementById('feedback');
const lista = document.getElementById('lista');
const btnAtualizar = document.getElementById('btn-atualizar');

function mostrarFeedback(mensagem, tipo) {
  feedback.textContent = mensagem;
  feedback.className = `feedback feedback--${tipo}`;
  feedback.hidden = false;
}

function esconderFeedback() {
  feedback.hidden = true;
}

function classeStamp(prioridade) {
  if (prioridade === 'Alta') return 'stamp--alta';
  if (prioridade === 'Media' || prioridade === 'Média') return 'stamp--media';
  if (prioridade === 'Baixa') return 'stamp--baixa';
  return 'stamp--pendente';
}

function formatarData(isoString) {
  const data = new Date(isoString);
  return data.toLocaleString('pt-BR', {
    day: '2-digit', month: '2-digit', year: 'numeric',
    hour: '2-digit', minute: '2-digit'
  });
}

async function carregarLista() {
  lista.innerHTML = '<p class="tickets__empty">Carregando…</p>';

  try {
    const resposta = await fetch('/solicitacoes/');
    if (!resposta.ok) throw new Error('Falha ao buscar solicitações.');

    const dados = await resposta.json();

    if (dados.length === 0) {
      lista.innerHTML = '<p class="tickets__empty">Nenhuma solicitação protocolada ainda.</p>';
      return;
    }

    lista.innerHTML = dados.map(renderizarTicket).join('');
  } catch (erro) {
    lista.innerHTML = '<p class="tickets__empty">Não foi possível carregar as solicitações.</p>';
  }
}

form.addEventListener('submit', async (evento) => {
  evento.preventDefault();
  esconderFeedback();

  const texto = textarea.value.trim();
  if (!texto) return;

  btnEnviar.disabled = true;
  btnEnviar.textContent = 'Enviando…';

  try {
    const resposta = await fetch('/solicitacoes/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ texto_original: texto })
    });

    const dados = await resposta.json();

    if (!resposta.ok) {
      mostrarFeedback(dados.erro || 'Erro ao protocolar solicitação.', 'erro');
      return;
    }

    if (dados.aviso) {
      mostrarFeedback(dados.aviso, 'aviso');
    } else {
      mostrarFeedback(`Solicitação #${String(dados.id).padStart(5, '0')} protocolada com sucesso.`, 'ok');
    }

    textarea.value = '';
    carregarLista();

  } catch (erro) {
    mostrarFeedback('Erro de conexão com o servidor.', 'erro');
  } finally {
    btnEnviar.disabled = false;
    btnEnviar.textContent = 'Protocolar solicitação';
  }
});

btnAtualizar.addEventListener('click', carregarLista);

carregarLista();

lista.addEventListener('click', async (evento) => {
  const botao = evento.target.closest('[data-excluir]');
  if (!botao) return;

  const id = botao.dataset.excluir;
  const confirmar = confirm(`Excluir a solicitação #${String(id).padStart(5, '0')}? Essa ação não pode ser desfeita.`);
  if (!confirmar) return;

  try {
    const resposta = await fetch(`/solicitacoes/${id}`, { method: 'DELETE' });

    if (!resposta.ok) {
      const dados = await resposta.json();
      mostrarFeedback(dados.erro || 'Erro ao excluir solicitação.', 'erro');
      return;
    }

    carregarLista();

  } catch (erro) {
    mostrarFeedback('Erro de conexão ao excluir solicitação.', 'erro');
  }
});