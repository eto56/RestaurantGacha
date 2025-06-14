const { Client, GatewayIntentBits } = require("discord.js");
const { fetch } = require('undici');
require('dotenv').config({ path: './../.env' });
const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,            // ギルド自体の接続を許可
    GatewayIntentBits.GuildMessages,     // ギルド内のメッセージ受信を許可
    GatewayIntentBits.MessageContent     // メッセージ内容の取得を許可
  ]
});


const msghandler = async (msg) => {
 if (!msg.content.startsWith("!")) return;
 
 const message = msg.content.slice(1);
 if (message == "help") {
  await msg.reply("駅名を入力してください。例: !新宿");
  return;
 }

 const station = message;
  const params = { station };
  console.log(params);

      try {
        const res = await fetch('http://backend:8080/search', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(params)
        });
        if (!res.ok) throw new Error('検索に失敗しました');
        const data = await res.json();
        const name = data.name
        const url = data.url

        await msg.reply(`店名: ${name}\nURL: ${url}`);
      } 
      catch (err) {
        await msg.reply("駅名を入力してください。例: !新宿");
        
      }
}

 

client.on("ready", () => console.log("Logged in"));
client.on("messageCreate", msghandler);
const token = process.env.DISCORD_TOKEN;
if (!token) {
  console.error("DISCORD_TOKENが設定されていません。");
  process.exit(1);
}
client.login(token);