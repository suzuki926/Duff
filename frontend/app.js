async function fetchProducts() {
  const res = await fetch('/products');
  const products = await res.json();
  const list = document.getElementById('products');
  list.innerHTML = '';
  products.forEach(p => {
    const li = document.createElement('li');
    li.textContent = `${p.id}: ${p.name} (${p.material})`;
    list.appendChild(li);
  });
}

document.getElementById('product-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  const payload = {
    name: document.getElementById('name').value,
    material: document.getElementById('material').value,
    manufacturing_place: document.getElementById('manufacturing_place').value,
    supply_chain_history: document.getElementById('supply_chain_history').value,
    recycling_info: document.getElementById('recycling_info').value
  };
  await fetch('/products', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  e.target.reset();
  fetchProducts();
});

fetchProducts();

async function fetchRequests() {
  const res = await fetch('/requests');
  const requests = await res.json();
  const list = document.getElementById('requests');
  list.innerHTML = '';
  requests.forEach(r => {
    const li = document.createElement('li');
    const urls = r.urls.map(u => `<a href="/requests/${r.id}?url=${u.url}">${u.url}</a>`).join(', ');
    li.innerHTML = `#${r.id} (tier ${r.tier}) - ${r.content} - URLs: ${urls} <button data-id="${r.id}">Escalate</button>`;
    list.appendChild(li);
  });
  document.querySelectorAll('#requests button').forEach(btn => {
    btn.addEventListener('click', async () => {
      await fetch(`/requests/${btn.dataset.id}/escalate`, { method: 'POST' });
      fetchRequests();
    });
  });
}

document.getElementById('request-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  const payload = { content: document.getElementById('content').value };
  await fetch('/requests', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  e.target.reset();
  fetchRequests();
});

fetchRequests();
