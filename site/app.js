const $ = id => document.getElementById(id);
const uniq = xs => [...new Set(xs)];
const esc = value => String(value ?? '').replace(/[&<>"']/g, char => ({
  '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
}[char]));

async function loadCatalog() {
  try {
    const response = await fetch('./products.json', {cache: 'no-cache'});
    if (!response.ok) throw new Error(`Catalog HTTP ${response.status}`);
    const data = await response.json();
    const videos = Object.fromEntries(data.videos.map(video => [video.id, video]));
    const names = product => uniq(product.offers.map(offer => videos[offer.video_id].channel));

    function priceSummary(product) {
      let values = product.offers.map(offer => offer.price).filter(Boolean);
      const estimated = values.filter(value => !value.startsWith('표시가 '));
      if (estimated.length) values = estimated;
      const seen = new Set();
      const prices = values.map(value => value.split('(')[0].trim()).filter(value => {
        const key = value.replace(/\s+/g, '').replace(/(만원|달러)대(?=초|중|후|극)/g, '$1')
          .replace(/(초반|중반|후반)대/g, '$1');
        if (seen.has(key)) return false;
        seen.add(key);
        return true;
      });
      return prices.length ? prices.slice(0, 3).join(' / ') + (prices.length > 3 ? ' …' : '') : '미공개';
    }

    function videoURL(offer) {
      const seconds = offer.time ? offer.time.split(':').reduce((sum, part) => sum * 60 + Number(part), 0) : null;
      return `https://www.youtube.com/watch?v=${encodeURIComponent(offer.video_id)}`
        + (seconds === null ? '' : `&t=${seconds}s`);
    }

    function codeHTML(offer) {
      if (!offer.code) return '<span class="muted">미공개</span>';
      let cell = `<code>${esc(offer.code)}</code>`;
      if (offer.code_url) {
        const url = new URL(offer.code_url);
        if (url.protocol === 'https:' && !url.username && !url.password) {
          cell = `<a href="${esc(url.href)}" target="_blank" rel="noreferrer">${cell}</a>`;
        }
      }
      return cell + (offer.code_note ? `<div class="muted">${esc(offer.code_note)}</div>` : '');
    }

    function shopHTML(offer) {
      try {
        const url = new URL(offer.url);
        const shop = url.hostname === 'aliexpress.com' || url.hostname.endsWith('.aliexpress.com');
        if (url.protocol !== 'https:' || !shop || url.username || url.password) return '';
        return `<div><a href="${esc(url.href)}" target="_blank" rel="noreferrer">알리에서 보기</a></div>`;
      } catch {
        return '';
      }
    }

    function productHTML(product) {
      const rows = product.offers.map(offer => `<tr>
        <td>${esc(videos[offer.video_id].channel)}</td>
        <td>${esc(offer.price || '미공개')}${offer.option ? `<div class="muted">${esc(offer.option)}</div>` : ''}${shopHTML(offer)}</td>
        <td>${codeHTML(offer)}</td>
        <td><a href="${esc(videoURL(offer))}" target="_blank" rel="noreferrer">${esc(offer.time || '영상')}</a></td>
      </tr>`).join('');
      return `<details class="product"><summary><span class="name">${esc(product.name)}</span>
        <span class="channels">[${esc(names(product).join(', '))}]</span>
        <span class="price">${esc(priceSummary(product))}</span></summary>
        <div class="table-wrap"><table><thead><tr>
          <th scope="col">유튜버</th><th scope="col">가격</th><th scope="col">할인 코드</th><th scope="col">영상</th>
        </tr></thead><tbody>${rows}</tbody></table></div></details>`;
    }

    function render() {
      const query = $('search').value.toLocaleLowerCase().trim();
      const category = $('category').value;
      const channel = $('channel').value;
      const products = data.products.filter(product => (!category || product.category === category)
        && (!channel || names(product).includes(channel))
        && (!query || [product.name, ...names(product)].join(' ').toLocaleLowerCase().includes(query)));
      const byChannel = $('group').value === 'channels';
      let groups = byChannel ? uniq(products.flatMap(names)) : uniq(products.map(product => product.category));
      if (byChannel && channel) groups = groups.filter(name => name === channel);
      if (byChannel) groups.sort((a, b) => a.localeCompare(b, 'ko'));
      $('count').textContent = `${products.length}종`;
      $('results').innerHTML = groups.length ? groups.map(group => {
        const items = products.filter(product => byChannel ? names(product).includes(group) : product.category === group);
        return `<section><h2>${esc(group)}</h2>${items.map(product => productHTML(byChannel
          ? {...product, offers: product.offers.filter(offer => videos[offer.video_id].channel === group)}
          : product)).join('')}</section>`;
      }).join('') : '<p class="muted">검색 결과가 없습니다.</p>';
    }

    $('category').innerHTML += uniq(data.products.map(product => product.category))
      .map(category => `<option>${esc(category)}</option>`).join('');
    $('channel').innerHTML += uniq(data.products.flatMap(names)).sort((a, b) => a.localeCompare(b, 'ko'))
      .map(channel => `<option>${esc(channel)}</option>`).join('');
    $('updated').textContent = '갱신 ' + new Intl.DateTimeFormat('ko-KR', {
      timeZone: 'Asia/Seoul', year: 'numeric', month: 'numeric', day: 'numeric',
      hour: '2-digit', minute: '2-digit', hour12: false
    }).format(new Date(data.updated_at));
    for (const id of ['search', 'group', 'category', 'channel']) {
      $(id).disabled = false;
      $(id).addEventListener(id === 'search' ? 'input' : 'change', render);
    }
    render();
  } catch (error) {
    $('results').textContent = '목록을 불러오지 못했습니다. 새로고침해 주세요.';
    console.error(error);
  }
}

loadCatalog();
