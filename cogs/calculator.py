import discord
from discord import app_commands
from discord.ext import commands  # noqa: F401

# I DIDN'T CODE THIS 
# CREDIT TO YOUTUBE/SANAMO
# https://www.youtube.com/@sanamopy
# https://github.com/sanamopy/discord.py-tutorials/tree/main/Episode%2014%20-%20Calculator

class Buttons(discord.ui.View):
    
  def __init__(self) -> None:
    super().__init__(timeout=180)
    self.expression = ""
    
  async def add(self, interaction: discord.Interaction, symbol) -> None:
    if self.expression == "Cleared!":
      self.expression =""
    self.expression += symbol
    await self.update(interaction)

  async def update(self, interaction: discord.Interaction) -> None:
    await interaction.response.defer()
    await interaction.message.edit(content=f"```{self.expression}```") #type: ignore

  async def solve(self, interaction: discord.Interaction) -> None:
    pi = 3.14159  # noqa: F841
    try:
      self.expression = str(eval(self.expression))
    except:  # noqa: E722
      await interaction.response.send_message("This expression is invalid", ephemeral=True)
    
    try:
      await self.update(interaction)
    except discord.InteractionResponded:
      pass
    self.expression = ""

  async def cleared(self, interaction: discord.Interaction) -> None:
    self.expression = "Cleared!"
    await self.update(interaction)

  @discord.ui.button(label="clear", style=discord.ButtonStyle.red, row=0)
  async def clear(self, interaction: discord.Interaction, Button: discord.ui.Button) -> None:
    await self.cleared(interaction)

  @discord.ui.button(label="(", style=discord.ButtonStyle.blurple, row=0)
  async def p1(self, interaction: discord.Interaction, Button: discord.ui.Button) -> None:
    await self.add(interaction, "(")

  @discord.ui.button(label=")", style=discord.ButtonStyle.blurple, row=0)
  async def p2(self, interaction: discord.Interaction, Button: discord.ui.Button) -> None:
    await self.add(interaction, ")")

  @discord.ui.button(label="/", style=discord.ButtonStyle.blurple, row=0)
  async def divide(self, interaction: discord.Interaction, Button: discord.ui.Button) -> None:
    await self.add(interaction, "/")

  @discord.ui.button(label="7", style=discord.ButtonStyle.grey, row=1)
  async def s7(self, interaction: discord.Interaction, Button: discord.ui.Button) -> None:
    await self.add(interaction, "7")

  @discord.ui.button(label="8", style=discord.ButtonStyle.grey, row=1)
  async def s8(self, interaction: discord.Interaction, Button: discord.ui.Button) -> None:
    await self.add(interaction, "8")

  @discord.ui.button(label="9", style=discord.ButtonStyle.grey, row=1)
  async def s9(self, interaction: discord.Interaction, Button: discord.ui.Button) -> None:
    await self.add(interaction, "9")

  @discord.ui.button(label="x", style=discord.ButtonStyle.blurple, row=1)
  async def multi(self, interaction: discord.Interaction, Button: discord.ui.Button) -> None:
    await self.add(interaction, "*")

  @discord.ui.button(label="4", style=discord.ButtonStyle.grey, row=2)
  async def s4(self, interaction: discord.Interaction, Button: discord.ui.Button) -> None:
    await self.add(interaction, "4")

  @discord.ui.button(label="5", style=discord.ButtonStyle.grey, row=2)
  async def s5(self, interaction: discord.Interaction, Button: discord.ui.Button) -> None:
    await self.add(interaction, "5")

  @discord.ui.button(label="6", style=discord.ButtonStyle.grey, row=2)
  async def s6(self, interaction: discord.Interaction, Button: discord.ui.Button) -> None:
    await self.add(interaction, "6")

  @discord.ui.button(label="-", style=discord.ButtonStyle.blurple, row=2)
  async def minus(self, interaction: discord.Interaction, Button: discord.ui.Button) -> None:
    await self.add(interaction, "-")

  @discord.ui.button(label="1", style=discord.ButtonStyle.grey, row=3)
  async def s1(self, interaction: discord.Interaction, Button: discord.ui.Button) -> None:
    await self.add(interaction, "1")

  @discord.ui.button(label="2", style=discord.ButtonStyle.grey, row=3)
  async def s2(self, interaction: discord.Interaction, Button: discord.ui.Button) -> None:
    await self.add(interaction, "2")

  @discord.ui.button(label="3", style=discord.ButtonStyle.grey, row=3)
  async def s3(self, interaction: discord.Interaction, Button: discord.ui.Button) -> None:
    await self.add(interaction, "3")

  @discord.ui.button(label="+", style=discord.ButtonStyle.blurple, row=3)
  async def plus(self, interaction: discord.Interaction, Button: discord.ui.Button) -> None:
    await self.add(interaction, "+")

  @discord.ui.button(label=".", style=discord.ButtonStyle.grey, row=4)
  async def decimal(self, interaction: discord.Interaction, Button: discord.ui.Button) -> None:
    await self.add(interaction, ".")

  @discord.ui.button(label="0", style=discord.ButtonStyle.grey, row=4)
  async def s0(self, interaction: discord.Interaction, Button: discord.ui.Button) -> None:
    await self.add(interaction, "0")

  @discord.ui.button(label="π", style=discord.ButtonStyle.grey, row=4)
  async def pi(self, interaction: discord.Interaction, Button: discord.ui.Button) -> None:
    await self.add(interaction, "pi")
  
  @discord.ui.button(label="=", style=discord.ButtonStyle.green, row=4)
  async def equals(self, interaction: discord.Interaction, Button: discord.ui.Button) -> None:
    await self.solve(interaction)


class cog2(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client
        
    @app_commands.command(name="calculator", description="Sends an interactive calculator")
    async def calculator(self, interaction: discord.Interaction):
        await interaction.response.send_message("```Begin Calculating```", view=Buttons())
        
async def setup(client: commands.Bot) -> None: 
    await client.add_cog(cog2(client))