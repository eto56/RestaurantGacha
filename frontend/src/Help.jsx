import React from 'react';

function Help() {
  return (
    <div className="container">
      <h1>Help / ヘルプ</h1>

      {/* English Section */}
      <div className="lang-section" style={{ textAlign: 'left' }}>
        <h2>How to Use (English)</h2>
        <p>This application helps you find a random restaurant based on your search criteria.</p>
        <ol>
          <li>
            <strong>Enter a station name:</strong> In the first input box, type the name of a train station in Japan (e.g., <code>Shinjuku</code>, <code>Shibuya</code>). This field is required.
          </li>
          <li>
            <strong>Enter a genre (optional):</strong> In the second input box, you can optionally specify a food genre (e.g., <code>Ramen</code>, <code>Izakaya</code>, <code>Sushi</code>).
          </li>
          <li>
            <strong>Search:</strong> Click the "Find Restaurant" button.
          </li>
          <li>
            <strong>Get a Result:</strong> The application will randomly select one restaurant that matches your search. The result will show the restaurant's name, its name in Kana, and a link to its official page on the HotPepper Gourmet website.
          </li>
        </ol>
      </div>

      {/* Japanese Section */}
      <div className="lang-section" style={{ textAlign: 'left' }}>
        <h2>使い方 (日本語)</h2>
        <p>このアプリケーションは、検索条件に基づいてランダムにレストランを見つけるのに役立ちます。</p>
        <ol>
          <li>
            <strong>駅名を入力:</strong> 最初の入力ボックスに、日本の駅名を入力してください（例: <code>新宿</code>、<code>渋谷</code>）。この項目は必須です。
          </li>
          <li>
            <strong>ジャンルを入力 (任意):</strong> 2番目の入力ボックスに、任意で料理のジャンルを指定できます（例: <code>ラーメン</code>、<code>居酒屋</code>、<code>寿司</code>）。
          </li>
          <li>
            <strong>検索:</strong> 「Find Restaurant」ボタンをクリックしてください。
          </li>
          <li>
            <strong>結果の表示:</strong> 検索条件に一致するレストランが1件、ランダムに選ばれて表示されます。結果には、レストランの名前、かな、そしてホットペッパーグルメの公式サイトへのリンクが表示されます。
          </li>
        </ol>
      </div>
    </div>
  );
}

export default Help;
