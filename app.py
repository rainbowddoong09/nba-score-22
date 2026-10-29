import streamlit as st
import streamlit.components.v1 as components

# 1. Streamlit 넓은 레이아웃 및 여백 제거
st.set_page_config(
    page_title="NBA 실시간 스코어보드",
    page_icon="🏀",
    layout="wide"
)

st.markdown("""
    <style>
        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 0rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            max-width: 100% !important;
        }
    </style>
""", unsafe_allow_html=True)

# 2. HTML / CSS / JS 코드 (실제 로스터 API 연동)
html_code = """
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>NBA 실시간 스코어보드</title>
  <link href="https://fonts.googleapis.com/css2?family=Pretendard:wght@400;600;700;800;900&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-color: #F5F2EB;
      --card-bg: #FAF8F5;
      --card-border: #E8E2D5;
      --text-main: #2C2A29;
      --text-muted: #7A7571;
      --accent-orange: #E65100;
      --accent-soft: #FFF3E0;
      --accent-green: #2E7D32;
      --shadow-sm: 0 4px 12px rgba(44, 42, 41, 0.05);
      --shadow-hover: 0 12px 28px rgba(230, 81, 0, 0.15);
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
    }

    body {
      background-color: var(--bg-color);
      color: var(--text-main);
      padding: 10px 0;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      width: 100%;
    }

    .container {
      width: 100%;
      max-width: 100%;
      padding: 0 15px;
    }

    header {
      text-align: center;
      margin-bottom: 20px;
    }

    header h1 {
      font-size: 2rem;
      font-weight: 900;
      color: var(--text-main);
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 10px;
    }

    header p {
      color: var(--text-muted);
      font-size: 0.95rem;
      margin-top: 4px;
    }

    .controls {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;
      padding: 0 10px;
    }

    .status-badge {
      font-size: 0.9rem;
      font-weight: 600;
      padding: 8px 16px;
      border-radius: 20px;
      background: #EFECE6;
      color: var(--text-muted);
    }

    .refresh-btn {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      color: var(--text-main);
      padding: 8px 18px;
      border-radius: 20px;
      font-weight: 700;
      font-size: 0.9rem;
      cursor: pointer;
      box-shadow: var(--shadow-sm);
      transition: all 0.2s ease;
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .refresh-btn:hover {
      background: var(--accent-orange);
      color: #FFF;
      border-color: var(--accent-orange);
      transform: translateY(-2px);
    }

    .games-list {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(450px, 1fr));
      gap: 20px;
      width: 100%;
    }

    .game-card {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 20px;
      padding: 24px;
      box-shadow: var(--shadow-sm);
      transition: transform 0.2s ease;
    }

    .game-card:hover {
      transform: translateY(-2px);
    }

    .matchup {
      display: grid;
      grid-template-columns: 1fr 100px 1fr;
      align-items: center;
      text-align: center;
    }

    .team-box {
      display: flex;
      flex-direction: column;
      align-items: center;
      cursor: pointer;
    }

    .logo-wrapper {
      width: 85px;
      height: 85px;
      border-radius: 50%;
      background: #FFFFFF;
      border: 2px solid var(--card-border);
      padding: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: var(--shadow-sm);
      transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }

    .logo-wrapper img {
      width: 100%;
      height: 100%;
      object-fit: contain;
    }

    .team-box:hover .logo-wrapper {
      transform: translateY(-6px) scale(1.08);
      border-color: var(--accent-orange);
      box-shadow: var(--shadow-hover);
    }

    .click-hint {
      font-size: 0.7rem;
      color: var(--accent-orange);
      margin-top: 4px;
      font-weight: 700;
      opacity: 0.8;
    }

    .team-name {
      font-size: 1.1rem;
      font-weight: 800;
      margin-top: 6px;
    }

    .score {
      font-size: 2.2rem;
      font-weight: 900;
      color: var(--accent-orange);
      margin-top: 2px;
    }

    .team-type {
      font-size: 0.75rem;
      font-weight: 700;
      color: var(--text-muted);
      letter-spacing: 1px;
    }

    .status-box {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 6px;
    }

    .game-status {
      font-size: 0.8rem;
      font-weight: 800;
      color: var(--accent-green);
      background: #E8F5E9;
      padding: 4px 10px;
      border-radius: 12px;
    }

    .vs-text {
      font-size: 1.1rem;
      font-weight: 900;
      color: var(--card-border);
    }

    details {
      margin-top: 18px;
      border-top: 1px dashed var(--card-border);
      padding-top: 14px;
    }

    summary {
      font-size: 0.85rem;
      font-weight: 700;
      color: var(--accent-orange);
      cursor: pointer;
      text-align: center;
      list-style: none;
    }

    summary::-webkit-details-marker {
      display: none;
    }

    .player-card {
      background: #FFFFFF;
      border: 1px solid var(--card-border);
      border-radius: 14px;
      padding: 12px 14px;
      margin-top: 10px;
      display: flex;
      align-items: center;
      gap: 14px;
    }

    .player-headshot {
      width: 55px;
      height: 55px;
      border-radius: 50%;
      object-fit: cover;
      background: #F5F2EB;
      border: 2px solid var(--accent-orange);
      flex-shrink: 0;
    }

    .player-info {
      flex: 1;
      text-align: left;
    }

    .player-name {
      font-size: 0.9rem;
      font-weight: 800;
    }

    .player-stat {
      font-size: 0.85rem;
      font-weight: 700;
      color: var(--accent-orange);
      margin-bottom: 4px;
    }

    .speech-bubble {
      background: var(--accent-soft);
      border: 1px solid #FFE0B2;
      border-radius: 8px;
      padding: 6px 10px;
      font-size: 0.8rem;
      color: var(--text-main);
      font-style: italic;
    }

    /* 모달 CSS */
    .modal-overlay {
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      background: rgba(44, 42, 41, 0.6);
      backdrop-filter: blur(6px);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 1000;
      opacity: 0;
      visibility: hidden;
      transition: all 0.3s ease;
      padding: 20px;
    }

    .modal-overlay.active {
      opacity: 1;
      visibility: visible;
    }

    .modal-content {
      background: #FAF8F5;
      border: 2px solid var(--card-border);
      border-radius: 24px;
      width: 100%;
      max-width: 620px;
      padding: 30px 24px;
      box-shadow: 0 20px 50px rgba(0,0,0,0.2);
      transform: translateY(30px) scale(0.95);
      transition: all 0.35s cubic-bezier(0.175, 0.885, 0.32, 1.275);
      position: relative;
      max-height: 90vh;
      overflow-y: auto;
    }

    .modal-overlay.active .modal-content {
      transform: translateY(0) scale(1);
    }

    .close-btn {
      position: absolute;
      top: 20px;
      right: 20px;
      background: #EFECE6;
      border: none;
      width: 36px;
      height: 36px;
      border-radius: 50%;
      font-size: 1.2rem;
      font-weight: 800;
      color: var(--text-muted);
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: all 0.2s;
    }

    .close-btn:hover {
      background: var(--accent-orange);
      color: #FFF;
    }

    .modal-header {
      text-align: center;
      margin-bottom: 24px;
    }

    .modal-team-logo {
      width: 70px;
      height: 70px;
      object-fit: contain;
      margin-bottom: 8px;
    }

    .modal-title {
      font-size: 1.4rem;
      font-weight: 900;
      color: var(--text-main);
    }

    .modal-subtitle {
      font-size: 0.85rem;
      font-weight: 700;
      color: var(--accent-orange);
      margin-top: 2px;
      letter-spacing: 1px;
    }

    .lineup-grid {
      display: flex;
      flex-direction: column;
      gap: 12px;
    }

    .lineup-card {
      background: #FFFFFF;
      border: 1px solid var(--card-border);
      border-radius: 16px;
      padding: 12px 18px;
      display: flex;
      align-items: center;
      gap: 16px;
      box-shadow: var(--shadow-sm);
      animation: fadeInUp 0.4s ease forwards;
    }

    .lineup-pos {
      background: var(--accent-soft);
      color: var(--accent-orange);
      border: 1px solid #FFE0B2;
      font-weight: 900;
      font-size: 0.85rem;
      padding: 6px 12px;
      border-radius: 10px;
      min-width: 45px;
      text-align: center;
    }

    .lineup-headshot {
      width: 50px;
      height: 50px;
      border-radius: 50%;
      object-fit: cover;
      background: #F5F2EB;
      border: 2px solid var(--accent-orange);
    }

    .lineup-info {
      flex: 1;
    }

    .lineup-name {
      font-size: 1rem;
      font-weight: 800;
      color: var(--text-main);
    }

    .lineup-detail {
      font-size: 0.85rem;
      color: var(--accent-orange);
      font-weight: 700;
      margin-top: 2px;
    }

    @keyframes fadeInUp {
      from {
        opacity: 0;
        transform: translateY(15px);
      }
      to {
        opacity: 1;
        transform: translateY(0);
      }
    }
  </style>
</head>
<body>
  <div class="container">
    <header>
      <h1>🏀 NBA 실시간 스코어</h1>
      <p>ESPN 라이브 연동 · 팀 로고를 클릭해 출전 선수를 확인하세요</p>
    </header>

    <div class="controls">
      <div id="statusBadge" class="status-badge">🔄 데이터 불러오는 중...</div>
      <button class="refresh-btn" onclick="fetchNBAScores()">🔄 새로고침</button>
    </div>

    <div id="gamesContainer" class="games-list"></div>
  </div>

  <div id="lineupModal" class="modal-overlay" onclick="closeModalOnBg(event)">
    <div class="modal-content">
      <button class="close-btn" onclick="closeModal()">✕</button>
      <div class="modal-header">
        <img id="modalLogo" class="modal-team-logo" src="" alt="Team Logo">
        <div id="modalTeamName" class="modal-title">Team Name</div>
        <div class="modal-subtitle">🏀 TEAM ROSTER & LINEUP</div>
      </div>
      <div id="modalLineupList" class="lineup-grid"></div>
    </div>
  </div>

  <script>
    let globalGamesData = [];

    async function fetchNBAScores() {
      const badge = document.getElementById('statusBadge');
      badge.textContent = '🔄 최신 경기 업데이트 중...';

      try {
        const res = await fetch('https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard');
        const data = await res.json();
        globalGamesData = data.events || [];

        badge.textContent = `📅 오늘 경기 (${globalGamesData.length}경기)`;
        renderGames(globalGamesData);
      } catch (err) {
        badge.textContent = '⚠️ ESPN 연결 실패 (CORS 재시도)';
        fetchViaProxy();
      }
    }

    async function fetchViaProxy() {
      try {
        const res = await fetch('https://api.allorigins.win/get?url=' + encodeURIComponent('https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard'));
        const wrapper = await res.json();
        const data = JSON.parse(wrapper.contents);
        globalGamesData = data.events || [];

        document.getElementById('statusBadge').textContent = `📅 오늘 경기 (${globalGamesData.length}경기)`;
        renderGames(globalGamesData);
      } catch (e) {
        document.getElementById('statusBadge').textContent = '❌ 데이터 수집 실패';
      }
    }

    function generateQuote(pts) {
      if (pts >= 35) return `🔥 오늘 폼 완전히 미쳤다! 혼자 ${pts}점 폭격!`;
      if (pts >= 25) return `⚡ 오늘 득점은 내가 다 책임진다! (${pts}점)`;
      if (pts > 0) return `🏀 승리를 위해 매 순간 최선을 다하는 중! (${pts}점)`;
      return "오늘 경기 꼭 승리한다! 준비 완료!";
    }

    function renderGames(games) {
      const container = document.getElementById('gamesContainer');
      if (!games.length) {
        container.innerHTML = `<div class="game-card" style="text-align:center; grid-column: 1 / -1;">오늘 예정된 NBA 경기가 없습니다.</div>`;
        return;
      }

      container.innerHTML = games.map((event, gameIdx) => {
        const competition = event.competitions[0];
        const statusText = event.status.type.detail || 'Scheduled';

        const home = competition.competitors.find(c => c.homeAway === 'home');
        const away = competition.competitors.find(c => c.homeAway === 'away');

        const getLeader = (comp) => {
          const leaders = comp.leaders || [];
          const ptsLeader = leaders.find(l => l.name === 'points') || leaders[0];
          if (ptsLeader && ptsLeader.leaders && ptsLeader.leaders[0]) {
            const l = ptsLeader.leaders[0];
            return {
              name: l.athlete.displayName,
              pts: parseInt(l.value || 0),
              headshot: l.athlete.headshot || 'https://a.espncdn.com/i/headshots/nba/players/full/fallback.png'
            };
          }
          return { name: `${comp.team.displayName} 에이스`, pts: 0, headshot: 'https://a.espncdn.com/i/headshots/nba/players/full/fallback.png' };
        };

        const homeLeader = getLeader(home);
        const awayLeader = getLeader(away);

        return `
          <div class="game-card">
            <div class="matchup">
              <!-- AWAY TEAM -->
              <div class="team-box" onclick="openLineupModal(${gameIdx}, 'away')">
                <div class="logo-wrapper">
                  <img src="${away.team.logo}" alt="${away.team.displayName}">
                </div>
                <div class="click-hint">🔍 로스터 보기</div>
                <div class="team-name">${away.team.shortDisplayName}</div>
                <div class="score">${away.score || 0}</div>
                <div class="team-type">AWAY</div>
              </div>

              <!-- STATUS -->
              <div class="status-box">
                <div class="game-status">${statusText}</div>
                <div class="vs-text">VS</div>
              </div>

              <!-- HOME TEAM -->
              <div class="team-box" onclick="openLineupModal(${gameIdx}, 'home')">
                <div class="logo-wrapper">
                  <img src="${home.team.logo}" alt="${home.team.displayName}">
                </div>
                <div class="click-hint">🔍 로스터 보기</div>
                <div class="team-name">${home.team.shortDisplayName}</div>
                <div class="score">${home.score || 0}</div>
                <div class="team-type">HOME</div>
              </div>
            </div>

            <!-- PLAYER DETAILS -->
            <details>
              <summary>🔥 팀별 최다 득점자 보기</summary>
              
              <div class="player-card">
                <img src="${awayLeader.headshot}" class="player-headshot" onerror="this.src='https://a.espncdn.com/i/headshots/nba/players/full/fallback.png'">
                <div class="player-info">
                  <div class="player-name">[AWAY] ${awayLeader.name}</div>
                  <div class="player-stat">${awayLeader.pts} PTS</div>
                  <div class="speech-bubble">"${generateQuote(awayLeader.pts)}"</div>
                </div>
              </div>

              <div class="player-card">
                <img src="${homeLeader.headshot}" class="player-headshot" onerror="this.src='https://a.espncdn.com/i/headshots/nba/players/full/fallback.png'">
                <div class="player-info">
                  <div class="player-name">[HOME] ${homeLeader.name}</div>
                  <div class="player-stat">${homeLeader.pts} PTS</div>
                  <div class="speech-bubble">"${generateQuote(homeLeader.pts)}"</div>
                </div>
              </div>
            </details>
          </div>
        `;
      }).join('');
    }

    /* -------------------------------------------
       실제 ESPN Summary API 로스터 수집 JS
    ------------------------------------------- */
    async function openLineupModal(gameIdx, teamType) {
      const event = globalGamesData[gameIdx];
      if (!event) return;

      const comp = event.competitions[0].competitors.find(c => c.homeAway === teamType);
      if (!comp) return;

      document.getElementById('modalLogo').src = comp.team.logo;
      document.getElementById('modalTeamName').textContent = comp.team.displayName;

      const lineupContainer = document.getElementById('modalLineupList');
      lineupContainer.innerHTML = `<div style="text-align:center; padding: 20px; color: var(--text-muted);">🔄 실제 선수 로스터를 불러오는 중...</div>`;
      document.getElementById('lineupModal').classList.add('active');

      try {
        // ESPN 경기 상세 Summary API 호출 (실제 선수 명단 포함)
        const summaryRes = await fetch(`https://site.api.espn.com/apis/site/v2/sports/basketball/nba/summary?event=${event.id}`);
        const summaryData = await summaryRes.json();
        
        let playerList = [];
        const defaultPositions = ['PG', 'SG', 'SF', 'PF', 'C'];

        if (summaryData.boxscore && summaryData.boxscore.players) {
          const teamBox = summaryData.boxscore.players.find(p => p.team.id === comp.team.id);
          if (teamBox && teamBox.statistics && teamBox.statistics[0]) {
            const athletes = teamBox.statistics[0].athletes || [];
            playerList = athletes.slice(0, 5).map((item, idx) => {
              const ath = item.athlete;
              const stats = item.stats || [];
              const pts = stats[0] || '0'; // 득점 수치
              return {
                name: ath.displayName,
                pos: ath.position ? ath.position.abbreviation : defaultPositions[idx],
                headshot: ath.headshot ? ath.headshot.href : 'https://a.espncdn.com/i/headshots/nba/players/full/fallback.png',
                jersey: ath.jersey ? `#${ath.jersey}` : '',
                ptsText: pts !== '0' ? `${pts} PTS` : 'Active Roster'
              };
            });
          }
        }

        // 만약 경기 전이라서 Boxscore 로스터가 없는 경우 Leader 데이터 활용
        if (playerList.length === 0 && comp.leaders) {
          comp.leaders.forEach((leaderGroup, idx) => {
            if (leaderGroup.leaders && leaderGroup.leaders[0]) {
              const l = leaderGroup.leaders[0];
              playerList.push({
                name: l.athlete.displayName,
                pos: defaultPositions[idx % 5],
                headshot: l.athlete.headshot || 'https://a.espncdn.com/i/headshots/nba/players/full/fallback.png',
                jersey: l.athlete.jersey ? `#${l.athlete.jersey}` : '',
                ptsText: `${l.value || 0} ${l.displayName || 'STAT'}`
              });
            }
          });
        }

        if (playerList.length > 0) {
          lineupContainer.innerHTML = playerList.map((p, i) => `
            <div class="lineup-card" style="animation-delay: ${i * 0.08}s">
              <div class="lineup-pos">${p.pos}</div>
              <img src="${p.headshot}" class="lineup-headshot" onerror="this.src='https://a.espncdn.com/i/headshots/nba/players/full/fallback.png'">
              <div class="lineup-info">
                <div class="lineup-name">${p.name} ${p.jersey}</div>
                <div class="lineup-detail">${p.ptsText}</div>
              </div>
            </div>
          `).join('');
        } else {
          lineupContainer.innerHTML = `<div style="text-align:center; padding: 20px;">경기 전이거나 선수 상세 정보를 준비 중입니다.</div>`;
        }

      } catch (err) {
        lineupContainer.innerHTML = `<div style="text-align:center; padding: 20px; color: var(--accent-orange);">선수 명단을 불러오는 중 오류가 발생했습니다.</div>`;
      }
    }

    function closeModal() {
      document.getElementById('lineupModal').classList.remove('active');
    }

    function closeModalOnBg(e) {
      if (e.target.id === 'lineupModal') {
        closeModal();
      }
    }

    fetchNBAScores();
    setInterval(fetchNBAScores, 30000);
  </script>
</body>
</html>
"""

# 3. Streamlit 화면 출력
components.html(html_code, height=1200, scrolling=True)
