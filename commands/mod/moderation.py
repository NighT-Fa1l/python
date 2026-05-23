import discord
from discord.ext import commands
from datetime import timedelta, datetime, timezone

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Kick command
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        try:
            await member.kick(reason=reason)
            await ctx.send(f"✅ {member.mention} has been kicked. Reason: {reason}")
        except Exception as e:
            await ctx.send(f"❌ Could not kick {member.mention}: {e}")

    # Ban command
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        try:
            await member.ban(reason=reason)
            await ctx.send(f"✅ {member.mention} has been banned. Reason: {reason}")
        except Exception as e:
            await ctx.send(f"❌ Could not ban {member.mention}: {e}")

    # Timeout command
    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def timeout(self, ctx, member: discord.Member, minutes: int, *, reason=None):
        try:
            duration = datetime.now(timezone.utc) + timedelta(minutes=minutes)
            await member.edit(timed_out_until=duration, reason=reason)
            await ctx.send(f"✅ {member.mention} has been timed out for {minutes} minutes. Reason: {reason}")
        except Exception as e:
            await ctx.send(f"❌ Could not timeout {member.mention}: {e}")

async def setup(bot):
    await bot.add_cog(Moderation(bot))
