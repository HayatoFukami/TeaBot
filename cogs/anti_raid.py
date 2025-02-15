import discord as d
from discord.ext import commands as cmds
import sqlite3
from collections import deque


class AntiRaid(cmds.Cog):
    def __init__(self, bot):
        self.bot = bot

        # データベース接続を確立
        self.con_anti_raid = sqlite3.connect("db\\anti_raid.sqlite")
        self.cur_anti_raid = self.con_anti_raid.cursor()

        # ギルドごとの参加時刻を保存する辞書
        # キーはguild.id、値は参加時刻のdeque
        self.join_times = {}

    def cog_unload(self):
        # コグがアンロードされる際にデータベース接続を閉じる
        self.conanti_raid.close()

    @cmds.Cog.listener("on_member_join")
    async def anti_raid(self, member: d.Member):
        guild = member.guild
        now = datetime.datetime.now()

        # サーバー設定を取得
        self.cur_anti_raid.execute("SELECT clm_count, clm_time FROM tbl_detection_settings WHERE clm_guild_id = ?", (guild.id,))
        result = self.cur_anti_raid.fetchone()

        # 設定が見つからない場合は何もしない
        if not result:
            return

        # 設定値を展開
        count, time = result

        # dequeを初期化、もしくは、既存のdequeを取得
        queue = self.join_times.setdefault(guild.id, deque(maxlen=count))

        # 参加時刻をqueueに追加
        queue.append(now)

        # 直近の参加時刻を取得
        recent_joins = [t for t in self.join_times[guild.id] if now - t < datetime.timedelta(seconds=time)]

        # レイド検知
        if len(recent_joins) >= count:
            print(f"Raid detected on {guild.name} ({guild.id})")

            # 招待を削除
            for invite in await guild.invites():
                await invite.delete(reason="Raid detected")

            # 最近参加したメンバーをキック
            for m in list(guild.members):
                if m.joined_at > now - datetime.timedelta(seconds=time):
                    try:
                        await m.kick(reason="Raid detected")
                        print(f"Kicked {m} from {guild.name} ({guild.id})")
                    except d.Forbidden:
                        print(f"Failed to kick {m} from {guild.name} ({guild.id})")
                    except d.HTTPException as e:
                        print(f"HTTP exception while kicking {m} from {guild.name} ({guild.id}): {e}")

            # 参加時刻キューをクリア
            queue.clear()


async def setup(bot: cmds.Bot):
    await bot.add_cog(AntiRaid(bot))
