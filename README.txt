아모르 웨딩 · Netlify 배포 패키지 (2026-10-07)

1. 빠른 수동 배포
- 먼저 dist 폴더를 Netlify의 수동 배포 영역에 드래그하면 홈페이지가 열립니다.
- 발급된 https://사이트명.netlify.app 또는 실제 연결할 도메인을 seo-config.json의 site_url에 입력합니다.
- 이 README가 있는 폴더에서 다음 명령을 실행합니다 (Python 3 필요):
  python3 tools/build.py
- 생성된 dist 폴더를 같은 Netlify 사이트에 다시 업로드하면 canonical, 절대경로 OG 이미지, sitemap.xml, robots.txt의 도메인 설정까지 완료됩니다.
- 수동 업로드는 Netlify에서 빌드 명령을 실행하지 않습니다. dist만 업로드하세요.

2. Git 연동 배포
- 이 프로젝트를 저장소에 올려 Netlify에 연결합니다.
- Build command: python3 tools/build.py / Publish directory: dist
- netlify.toml에 설정되어 있습니다. Netlify의 URL 환경변수로 대표 도메인을 자동 적용합니다.
- 별도 도메인을 지정하려면 SITE_URL 환경변수 또는 seo-config.json의 site_url을 설정하세요.
- 도메인 변경 시 재빌드·재배포하세요.

3. 검색 노출
- 제목·설명, OG/Twitter 공유 이미지, 한국어 언어 정보, 사업자/서비스 구조화 데이터, robots.txt를 적용했습니다.
- 실제 도메인이 제공되지 않아 최초 dist에는 canonical과 sitemap.xml을 임의 도메인으로 넣지 않았습니다. 위 1 또는 2의 도메인 적용으로 완성됩니다.
- privacy 페이지는 검색 결과 제외(noindex), 홈페이지만 sitemap에 등록합니다.
- Naver Search Advisor / Google Search Console 소유확인 토큰은 seo-config.json의 해당 값에 입력 후 재빌드하세요. 소유확인과 사이트맵 제출은 사이트 소유자 계정에서 진행합니다.
- 검색 순위·색인 시점은 검색엔진이 결정합니다.

4. 수정 사항
- Scroll to explore 화살표의 아래 방향 반복 모션 및 동작 줄이기 대응
- BASIC/PREMIUM/VIP 화면과 검색 메타데이터·구조화 데이터에서 스드메 삭제
- 상담 버튼 아래 개인정보 링크 문구 삭제
- 주소, 대표자, 전화번호, 사업자번호 반영 / 영업시간·SNS 삭제
- 개인정보처리방침 링크 밑줄 제거 / 동의 안내 링크·페이지 삭제(기존 주소는 방침으로 이동)
- 개인정보처리방침 사업자·문의 정보 반영, Netlify 호스팅 안내
- 로고 기반 1200×630 OG 이미지 assets/og-amor.jpg 포함
- 404 페이지, 보안 응답 헤더, 정적 배포 폴더 포함

5. 개인정보 운영 확인
- 알려주신 브랜드명을 사업자명으로 반영했습니다. 사업자등록증의 상호가 다르면 수정하세요.
- 최도준 대표를 개인정보 문의 접수자로 반영했습니다. 실제 개인정보 보호책임자 지정 여부는 운영자가 확인해야 합니다.
- 시행일은 수정일인 2026-10-07입니다. 실제 적용일이 다르면 privacy.html을 수정하세요.
- 상담정보 보유·파기 기준과 보호조치는 기존 문안의 운영 기준입니다. 실제 상담 운영과 일치하는지 확인하세요.
- Netlify 계약·요금제·서버 및 운영 도구가 확정되지 않아 국외이전 국가·수탁자/재수탁자·보유기간 등은 추정해 넣지 않았습니다. 실제 계약에 따른 필수 고지사항을 배포 전 확인해야 합니다. 외부 정책 링크만으로 운영자의 고지 의무가 모두 충족되는 것은 아닙니다.
- 수집·이용 동의 안내 링크 삭제와 상담 시 필요한 동의 절차는 별개입니다. 기존 카카오 상담 동의 예시는 docs에 보관했습니다(공개 dist에 미포함).

참고 문서
https://docs.netlify.com/deploy/create-deploys/
https://docs.netlify.com/build/configure-builds/environment-variables/
https://www.netlify.com/privacy/

OG 제작: 기존 AMOR 로고를 참조한 내장 이미지 생성 도구.
프롬프트: 기존 하트·무한대 심볼과 AMOR 글자를 보존하고, 아이보리 종이 질감 배경과 딥그린 로고를 중앙에 배치한 미니멀 웨딩 공유 카드. 추가 문구 없음.
