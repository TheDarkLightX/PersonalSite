/* Presentation adapter for the Authority-recorded table. No server authority. */
(() => {
  'use strict';
  const names = Object.freeze({160:'Nobody',161:'Alice',162:'Bob',163:'Carol'});
  const labels = Object.freeze({150:'Pending',151:'Approved',152:'Cancelled'});
  const reasons = Object.freeze({200:'This request is closed.',201:'Nobody is not an approver.',
    202:'Cancellation was recorded. No release was requested.',203:'The same approver cannot supply both keys.'});
  const el = id => document.getElementById(id);
  const buttons = [...document.querySelectorAll('[data-action]')];
  let table, state = [150,160,160], releases = 0, actions = 0;

  function paint() {
    el('desk-status').textContent = labels[state[0]];
    el('desk-status').dataset.state = state[0];
    el('first-key').textContent = state[1] === 160 ? 'Waiting' : names[state[1]];
    el('second-key').textContent = state[2] === 160 ? 'Waiting' : names[state[2]];
    el('release-count').textContent = String(releases);
    el('action-count').textContent = String(actions);
  }

  function reset() {
    state = [150,160,160]; releases = 0; actions = 0;
    el('desk-history').replaceChildren();
    el('decision-json').textContent = 'Choose an action to inspect its recorded decision.';
    el('desk-result').textContent = 'New simulated request. Two different approver IDs are required.';
    el('desk-result').dataset.kind = 'ready'; paint();
  }

  function act(command, officer) {
    if (!table || ![140,141].includes(command) || ![160,161,162,163].includes(officer)) return;
    const input = [...state, command, officer];
    const decision = table.get(input.join(','));
    if (!decision) {
      el('desk-result').textContent = 'No checked table row for this input. Nothing changed.';
      el('desk-result').dataset.kind = 'Reject'; return;
    }
    const previous = [...state];
    if (decision.class === 'Accept' || decision.class === 'CommittedFailure') {
      state = decision.post.map(f => f.value.variant);
      releases += decision.outbox.length;
    }
    actions += 1;
    const message = reasons[decision.reason] || (decision.outbox?.length
      ? 'Second key accepted. One release intent was recorded.'
      : decision.class === 'refused' ? 'A contract law refused this decision. Nothing changed.'
      : 'First key recorded. A different approver must supply the second.');
    el('desk-result').textContent = `${decision.class}: ${message}`;
    el('desk-result').dataset.kind = decision.class;
    const item = document.createElement('li');
    item.textContent = `${actions}. ${names[officer]} · ${command === 140 ? 'Approve' : 'Cancel'} → ${decision.class}. ${message}`;
    el('desk-history').prepend(item);
    // Bound presentation memory; no policy decision depends on displayed history.
    while (el('desk-history').children.length > 40) el('desk-history').lastChild.remove();
    el('decision-json').textContent = JSON.stringify({input, previous, decision, next:state}, null, 2);
    paint();
  }

  buttons.forEach(button => button.addEventListener('click', () => {
    if (button.dataset.action === 'reset') reset();
    else act(Number(button.dataset.action), Number(el('desk-officer').value));
  }));
  document.querySelectorAll('[data-scenario]').forEach(button => button.addEventListener('click', () => {
    if (!table) return;
    reset();
    const sequences = {repeat:[[140,161],[140,161],[140,162],[140,163]],
      cancel:[[140,161],[141,162],[140,163]], unknown:[[140,160]]};
    for (const [command, officer] of sequences[button.dataset.scenario]) act(command, officer);
  }));
  fetch('./decision-table.json').then(response => {
    if (!response.ok) throw new Error('Table unavailable'); return response.json();
  }).then(data => {
    if (data.schema !== 'two-key-release/demo-table/1' || data.rows.length !== 384 ||
        data.framework_commit !== 'a1ce03e2bcd917ecb9a61a29be429f5ca09a85b8') throw new Error('Unexpected table');
    table = new Map(data.rows.map(row => [row.input.join(','), row]));
    if (table.size !== 384) throw new Error('Duplicate table input');
    buttons.forEach(button => button.disabled = false);
    document.querySelectorAll('[data-scenario]').forEach(button => button.disabled = false);
    reset();
  }).catch(() => { el('desk-result').textContent = 'The decision table could not be loaded. Controls remain disabled.'; });
})();
