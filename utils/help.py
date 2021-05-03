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

    def get_opening_note(self):
        command_name = self.invoked_with
        return (
            f"Use `{self.context.prefix}{command_name} [command]` for more info on a command.\n"
            f"You can also use `{self.context.prefix}{command_name} [category]` for more info on a category."
        )

    async def send_bot_help(self, mapping):
        cogs_embed = discord.Embed(title="All Categories")
        cogs_embed.set_footer(text=self.get_opening_note())
        commands_embeds = []
        for cog,cmds in mapping.items():
            cogs_embed.add_field(name=getattr(cog, "qualified_name", "No category"), value="\n".join(x.name for x in cmds), inline=False)
            command_embed = discord.Embed(title=getattr(cog, "qualified_name", "No category"))
            for cmd in cmds:
                description = cmd.brief or "No description"
                command_embed.add_field(name=cmd.name,value = f"{description}\n`{self.get_command_signature(cmd)}`")
            commands_embeds.append(command_embed)
        commands_embeds.insert(0, cogs_embed)
        page = menus.MenuPages(source=PageSource(commands_embeds))
        await page.start(self.context)


