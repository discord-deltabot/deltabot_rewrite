import discord
from discord.ext import commands, menus


class PageSource(menus.ListPageSource):
    def __init__(self, data):
        super(PageSource, self).__init__(data, per_page=1)

    async def format_page(self, menu, page):
        return page


# noinspection PyShadowingNames
class MyHelp(commands.HelpCommand):
    def get_command_signature(self, command):
        return '%s%s %s' % (self.clean_prefix, command.qualified_name, command.signature)

    async def send_bot_help(self, mapping):
        cogs_embed = discord.Embed(title="All Categories")
        commands_embed = []
        for cog,cmds in mapping.items():
            cogs_embed.add_field(name=getattr(cog, "qualified_name", "No category"), value="\n".join(x.name for x in cmds))
            command_embed = discord.Embed(title=getattr(cog, "qualified_name", "No category"))
            for cmd in cmds:
                command_embed.add_field(name=cmd.name,value=getattr(cmd, "brief", "No help available"))
                commands_embed.append(command_embed)
            commands_embed.insert(0, cogs_embed)
        page = menus.MenuPages(source=PageSource(commands_embed))
        await page.start(self.context)


