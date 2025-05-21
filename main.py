import disnake
from disnake.ext import commands
import datetime
import asyncio

bot = commands.Bot(command_prefix='.', help_command=None, intents=disnake.Intents.all(), test_guilds=[1254760924770865183])

base_role_id = 0 # past it
announcement_channel_id = 0 # past it
forbidden_words = [] 
forbidden_words = []
with open("fwords.txt", "r", encoding="utf-8") as file:
    for line in file:
        forbidden_words.append(line.strip())


@bot.event
async def on_ready():
    print(f'{bot.user} is ready to work!')
    guild_id = 0 # past it
    channel_id = announcement_channel_id 

    guild = bot.get_guild(guild_id)  
    channel = bot.get_channel(channel_id) 

    if guild and channel:
        await channel.send("Привет всем! Я в сети!")
    else:
        print("Не удалось найти сервер или канал для приветствия.") 

@bot.event
async def on_member_join(member):
    """
    Эта функция будет вызываться каждый раз, когда новый пользователь заходит на сервер.
    """
    
    role = member.guild.get_role(base_role_id)
    if role:
        await member.add_roles(role)
        print(f"Роль {role.name} успешно выдана пользователю {member.name}")

        announcement_channel = bot.get_channel(announcement_channel_id)  
        if announcement_channel:
            await announcement_channel.send(f"Приветствуем на сервере, {member.mention}!")
    else:
        print(f"Роль с ID {base_role_id} не найдена!")


@bot.event
async def on_message(message):
    """
    Эта функция будет вызываться каждый раз, когда отправляется новое сообщение.
    """

    if message.author == bot.user:
        return

    message_content = message.content.lower()
    message_content = message_content.replace(" ", "")

    for word in forbidden_words:
        if word in message_content:
            await message.delete()  # Удаляем сообщение
            await message.channel.send(f"{message.author.mention}, на этом сервере запрещено использовать ненормативную лексику!")
            return 

    await bot.process_commands(message) 


@bot.command(name="выгнать", aliases=['kick'])
@commands.has_permissions(kick_members=True)  
async def kick(ctx, member: disnake.Member, *, reason=None):
    """
    Выгоняет участника с сервера.

    """

    await member.kick(reason=reason)
    await ctx.send(f"Участник {member.mention} был выгнан с сервера. Причина: {reason}")


import disnake
from disnake.ext import commands


@bot.slash_command(name="выгнать", description="Выгоняет участника с сервера.")
@commands.has_permissions(kick_members=True)
async def kick(inter: disnake.ApplicationCommandInteraction, member: disnake.Member, reason: str = None):
    """
    Выгоняет участника с сервера (слэш-команда).
    """

    await member.kick(reason=reason)
    await inter.response.send_message(f"Участник {member.mention} был выгнан с сервера. Причина: {reason}")


@bot.command(name="забанить", aliases=['ban'])
@commands.has_permissions(ban_members=True)  
async def ban(ctx, member: disnake.Member, *, reason=None):
    """
    Банит участника на сервере.

    """

    await member.ban(reason=reason)
    await ctx.send(f"Участник {member.mention} был забанен на сервере. Причина: {reason}")


import disnake
from disnake.ext import commands


@bot.slash_command(name="забанить", description="Банит участника на сервере.")
@commands.has_permissions(ban_members=True)
async def ban(inter: disnake.ApplicationCommandInteraction, member: disnake.Member, reason: str = None):
    """
    Банит участника на сервере (слэш-команда).
    """

    await member.ban(reason=reason)
    await inter.response.send_message(f"Участник {member.mention} был забанен на сервере. Причина: {reason}")


@bot.command(name="таймаут", aliases=['timeout'])
@commands.has_permissions(moderate_members=True) 
async def timeout(ctx, member: disnake.Member, duration: int, time_unit: str, *, reason=None):
    """
    Отправляет участника в тайм-аут.
    """

    time_units = {"секунд": 1, "минут": 60, "часов": 3600, "дней": 86400}  

    if time_unit.lower() in time_units:
        seconds = duration * time_units[time_unit.lower()]
        end_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=seconds)

        try:
            await member.edit(timeout=end_time, reason=reason)
            await ctx.send(f"Участнику {member.mention} выдан тайм-аут на {duration} {time_unit}. Причина: {reason}")
        except disnake.Forbidden:
            await ctx.send("У меня недостаточно прав, чтобы выдать тайм-аут этому участнику.")
        except disnake.HTTPException as e:
            await ctx.send(f"Произошла ошибка при выдаче тайм-аута: {e}")
    else:
        await ctx.send(f"Неверная единица времени. Доступные варианты: секунды, минуты, часы, дни")


@bot.slash_command(name="таймаут", description="Отправляет участника в тайм-аут.")
@commands.has_permissions(moderate_members=True)
async def timeout(inter: disnake.ApplicationCommandInteraction, member: disnake.Member, duration: int, time_unit: str, reason: str = None):
    """
    Отправляет участника в тайм-аут (слэш-команда).
    """

    time_units = {"секунд": 1, "минут": 60, "часов": 3600, "дней": 86400}

    if time_unit.lower() in time_units:
        seconds = duration * time_units[time_unit.lower()]
        end_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=seconds)

        try:
            await member.edit(timeout=end_time, reason=reason)
            await inter.response.send_message(f"Участнику {member.mention} выдан тайм-аут на {duration} {time_unit}. Причина: {reason}")
        except disnake.Forbidden:
            await inter.response.send_message("У меня недостаточно прав, чтобы выдать тайм-аут этому участнику.")
        except disnake.HTTPException as e:
            await inter.response.send_message(f"Произошла ошибка при выдаче тайм-аута: {e}")
    else:
        await inter.response.send_message(f"Неверная единица времени. Доступные варианты: секунды, минуты, часы, дни")


@bot.command(name="роль", aliases=["инфо_роли", "roleinfo"])
async def role_info(ctx, *, role: disnake.Role):
    """
    Выводит информацию о роли.

    Пример:
    .роль @Роль
    """

    embed = disnake.Embed(
        title=f"Информация о роли: {role.name}",
        color=role.color,
    )

    embed.add_field(name="ID роли:", value=role.id, inline=False)
    embed.add_field(name="Цвет роли:", value=str(role.color), inline=False)
    embed.add_field(name="Создана:", value=role.created_at.strftime("%d.%m.%Y %H:%M:%S"), inline=False)
    embed.add_field(name="Позиция:", value=role.position, inline=False)
    embed.add_field(name="Упоминаемая:", value="Да" if role.mentionable else "Нет", inline=False)
    embed.add_field(name="Количество участников с этой ролью:", value=len(role.members), inline=False)

    permissions = [perm[0] for perm in role.permissions if perm[1]]
    if permissions:
        embed.add_field(name="Права:", value=", ".join(permissions), inline=False)
    else:
        embed.add_field(name="Права:", value="Нет", inline=False)

    await ctx.send(embed=embed)


import disnake
from disnake.ext import commands


@bot.slash_command(name="роль", description="Выводит информацию о роли.")
async def role_info(inter: disnake.ApplicationCommandInteraction, role: disnake.Role):
    """
    Выводит информацию о роли (слэш-команда).
    """

    embed = disnake.Embed(
        title=f"Информация о роли: {role.name}",
        color=role.color,
    )

    embed.add_field(name="ID роли:", value=role.id, inline=False)
    embed.add_field(name="Цвет роли:", value=str(role.color), inline=False)
    embed.add_field(name="Создана:", value=role.created_at.strftime("%d.%m.%Y %H:%M:%S"), inline=False)
    embed.add_field(name="Позиция:", value=role.position, inline=False)
    embed.add_field(name="Упоминаемая:", value="Да" if role.mentionable else "Нет", inline=False)
    embed.add_field(name="Количество участников с этой ролью:", value=len(role.members), inline=False)

    permissions = [perm[0] for perm in role.permissions if perm[1]]
    if permissions:
        embed.add_field(name="Права:", value=", ".join(permissions), inline=False)
    else:
        embed.add_field(name="Права:", value="Нет", inline=False)

    await inter.response.send_message(embed=embed)


@bot.command(name="участники_роли", aliases=["members"])
async def list_role_members(ctx, *, role: disnake.Role):
  """
  Выводит список участников с указанной ролью.
  """

  if not role.members:
    await ctx.send(f"У роли {role.mention} нет участников.")
    return

  members_list = "\n".join([member.mention for member in role.members])
  embed = disnake.Embed(title=f"Участники роли {role.name}:", description=members_list, color=role.color)
  await ctx.send(embed=embed)


@bot.slash_command(name="участники_роли", description="Выводит список участников с указанной ролью.")
async def list_role_members(inter: disnake.ApplicationCommandInteraction, role: disnake.Role):
  """
  Выводит список участников с указанной ролью (слэш-команда).
  """

  if not role.members:
    await inter.response.send_message(f"У роли {role.mention} нет участников.")
    return

  members_list = "\n".join([member.mention for member in role.members])
  embed = disnake.Embed(title=f"Участники роли {role.name}:", description=members_list, color=role.color)
  await inter.response.send_message(embed=embed)

@bot.command(name="инфо", aliases=["userinfo"])
async def user_info(ctx, member: disnake.Member = None):
    """
    Выводит информацию о пользователе.
    """

    member = member or ctx.author 

    embed = disnake.Embed(title=f"Информация о пользователе {member.name}", color=member.color)

    embed.add_field(name="Имя на сервере:", value=member.display_name, inline=False)
    embed.add_field(name="ID пользователя:", value=member.id, inline=False)
    embed.add_field(name="Аккаунт создан:", value=member.created_at.strftime("%d.%m.%Y %H:%M:%S"), inline=False)
    embed.add_field(name="Присоединился к серверу:", value=member.joined_at.strftime("%d.%m.%Y %H:%M:%S"), inline=False)
    embed.add_field(name="Высшая роль:", value=member.top_role.mention, inline=False)
    embed.add_field(name="Бот:", value="Да" if member.bot else "Нет", inline=False)

    embed.set_thumbnail(url=member.avatar.url)
    await ctx.send(embed=embed)


@bot.slash_command(name="инфо", description="Выводит информацию о пользователе.")
async def user_info(inter: disnake.ApplicationCommandInteraction, member: disnake.Member = None):
    """
    Выводит информацию о пользователе (слэш-команда).
    """

    member = member or inter.author

    embed = disnake.Embed(title=f"Информация о пользователе {member.name}", color=member.color)

    embed.add_field(name="Имя на сервере:", value=member.display_name, inline=False)
    embed.add_field(name="ID пользователя:", value=member.id, inline=False)
    embed.add_field(name="Аккаунт создан:", value=member.created_at.strftime("%d.%m.%Y %H:%M:%S"), inline=False)
    embed.add_field(name="Присоединился к серверу:", value=member.joined_at.strftime("%d.%m.%Y %H:%M:%S"), inline=False)
    embed.add_field(name="Высшая роль:", value=member.top_role.mention, inline=False)
    embed.add_field(name="Бот:", value="Да" if member.bot else "Нет", inline=False)

    embed.set_thumbnail(url=member.avatar.url)
    await inter.response.send_message(embed=embed) # Отправка ответа


import disnake
from disnake.ext import commands


@bot.command(name="сервер", aliases=["serverinfo"])
async def server_info(ctx):
    """
    Выводит информацию о сервере.
    """

    guild = ctx.guild 

    embed = disnake.Embed(
        title=f"Информация о сервере {guild.name}",
        color=disnake.Color.blue()
    )

    embed.add_field(name="ID:", value=guild.id, inline=False)
    embed.add_field(name="Владелец:", value=guild.owner.mention, inline=False)
    embed.add_field(name="Создан:", value=guild.created_at.strftime("%d.%m.%Y %H:%M:%S"), inline=False)
    embed.add_field(name="Участников:", value=guild.member_count, inline=False)
    embed.add_field(name="Текстовых каналов:", value=len(guild.text_channels), inline=False)
    embed.add_field(name="Голосовых каналов:", value=len(guild.voice_channels), inline=False)
    embed.add_field(name="Ролей:", value=len(guild.roles), inline=False)

    embed.set_thumbnail(url=guild.icon.url if guild.icon else None)  
    await ctx.send(embed=embed)


@bot.slash_command(name="сервер", description="Выводит информацию о сервере.")
async def server_info(inter: disnake.ApplicationCommandInteraction):
    """
    Выводит информацию о сервере (слэш-команда).
    """

    guild = inter.guild  

    embed = disnake.Embed(
        title=f"Информация о сервере {guild.name}",
        color=disnake.Color.blue()
    )

    embed.add_field(name="ID:", value=guild.id, inline=False)
    embed.add_field(name="Владелец:", value=guild.owner.mention, inline=False)
    embed.add_field(name="Создан:", value=guild.created_at.strftime("%d.%m.%Y %H:%M:%S"), inline=False)
    embed.add_field(name="Участников:", value=guild.member_count, inline=False)
    embed.add_field(name="Текстовых каналов:", value=len(guild.text_channels), inline=False)
    embed.add_field(name="Голосовых каналов:", value=len(guild.voice_channels), inline=False)
    embed.add_field(name="Ролей:", value=len(guild.roles), inline=False)
    embed.set_thumbnail(url=guild.icon.url if guild.icon else None)  

    await inter.response.send_message(embed=embed)


@bot.command(name="дай_роль", aliases=["add_role"])
@commands.has_permissions(manage_roles=True)
async def give_role(ctx, member: disnake.Member, *, role: disnake.Role):
    """
    Выдаёт роль пользователю.

    Пример:
    .дай_роль @username @НазваниеРоли
    """
    
    if role in member.roles:
        await ctx.send(f"У пользователя {member.mention} уже есть роль {role.mention}")
        return

    await member.add_roles(role)
    await ctx.send(f"Роль {role.mention} успешно выдана пользователю {member.mention}")


@bot.slash_command(name="дай_роль", description="Выдаёт роль пользователю.")
@commands.has_permissions(manage_roles=True)
async def give_role(inter: disnake.ApplicationCommandInteraction, member: disnake.Member, role: disnake.Role):
    """
    Выдаёт роль пользователю (слэш-команда).
    """
    
    if role in member.roles:
        await inter.response.send_message(f"У пользователя {member.mention} уже есть роль {role.mention}")
        return
    
    await member.add_roles(role)
    await inter.response.send_message(f"Роль {role.mention} успешно выдана пользователю {member.mention}")


@bot.command(name="забери_роль", aliases=["remove_role"])
@commands.has_permissions(manage_roles=True)
async def remove_role(ctx, member: disnake.Member, *, role: disnake.Role):
    """
    Забирает роль у пользователя.

    Пример:
    .забери_роль @username @НазваниеРоли
    """

    if role not in member.roles:
        await ctx.send(f"У пользователя {member.mention} нет роли {role.mention}")
        return

    await member.remove_roles(role)
    await ctx.send(f"Роль {role.mention} успешно убрана у пользователя {member.mention}")



@bot.slash_command(name="забери_роль", description="Забирает роль у пользователя.")
@commands.has_permissions(manage_roles=True)
async def remove_role(inter: disnake.ApplicationCommandInteraction, member: disnake.Member, role: disnake.Role):
    """
    Забирает роль у пользователя (слэш-команда).
    """

    if role not in member.roles:
        await inter.response.send_message(f"У пользователя {member.mention} нет роли {role.mention}")
        return

    await member.remove_roles(role)
    await inter.response.send_message(f"Роль {role.mention} успешно убрана у пользователя {member.mention}")


async def get_ban_list(guild_id: int):
  """
  Возвращает список забаненных пользователей на сервере.

  Args:
      guild_id: ID сервера Discord.

  Returns:
      Список объектов `disnake.BanEntry`, представляющих забаненных пользователей.
  """
  guild = bot.get_guild(guild_id)
  if guild:
    # Правильно обрабатываем асинхронный итератор
    bans = [ban async for ban in guild.bans()]
    return bans
  else:
    return None


@bot.command()
@commands.has_permissions(ban_members=True)
async def banlist(ctx):
    """
    Показывает список забаненных пользователей на сервере.
    """
    bans = await get_ban_list(ctx.guild.id)

    if bans:
      embed = disnake.Embed(title="Список забаненных пользователей", color=disnake.Color.red())
      for ban in bans:
        embed.add_field(name=f"{ban.user.name}#{ban.user.discriminator}", value=f"Причина: {ban.reason}", inline=False)
      await ctx.send(embed=embed)
    else:
      await ctx.send("На этом сервере нет забаненных пользователей.")


@bot.slash_command(name="банлист", description="Показывает список забаненных пользователей на сервере.")
@commands.has_permissions(ban_members=True) # Ограничиваем доступ к команде
async def banlist(inter: disnake.ApplicationCommandInteraction):
    """
    Показывает список забаненных пользователей на сервере.
    """
    await inter.response.defer() # Откладываем ответ, чтобы избежать ошибки "interaction failed"
    bans = await get_ban_list(inter.guild.id)

    if bans:
      embed = disnake.Embed(title="Список забаненных пользователей", color=disnake.Color.red())
      for ban in bans:
        embed.add_field(name=f"{ban.user.name}#{ban.user.discriminator}", value=f"Причина: {ban.reason}", inline=False)
      await inter.edit_original_message(embed=embed) # Изменяем отложенный ответ
    else:
      await inter.edit_original_message(content="На этом сервере нет забаненных пользователей.")


async def unban_user(guild_id: int, user_id: int):
  """
  Разбанивает пользователя на сервере.

  Args:
      guild_id: ID сервера Discord.
      user_id: ID пользователя, которого нужно разбанить.

  Returns:
      True, если пользователь был успешно разбанен, 
      False, если пользователь не был найден в списке забаненных.
  """
  guild = bot.get_guild(guild_id)
  if guild:
    try:
      await guild.unban(disnake.Object(id=user_id))
      return True
    except disnake.NotFound:
      return False
  else:
    return False


@bot.slash_command(name="разбань", description="Разбанивает пользователя на сервере.")
@commands.has_permissions(ban_members=True)
async def unban(inter: disnake.ApplicationCommandInteraction, user_id):
       """
       Разбанивает пользователя на сервере.
       """
       try:
           user_id = int(user_id)
       except ValueError:
           await inter.response.send_message("Неверный формат ID пользователя. Пожалуйста, введите число.", ephemeral=True)
           return

       await inter.response.defer()

       if await unban_user(inter.guild.id, user_id):
           await inter.edit_original_message(content=f"Пользователь с ID {user_id} успешно разбанен.")
       else:
           await inter.edit_original_message(content=f"Пользователь с ID {user_id} не найден в списке забаненных.")


@bot.slash_command(name="пригласить", description="Создает ссылку-приглашение на сервер.")
async def create_invite(inter: disnake.ApplicationCommandInteraction, 
                       max_hours: int = 0, 
                       max_uses: int = 0): 
    """
    Генерирует ссылку-приглашение на сервер с заданными ограничениями.

    Параметры:
      max_hours: Время действия ссылки в часах (0 = неограничено).
      max_uses: Максимальное количество использований ссылки (0 = неограничено).
    """


    max_age_seconds = max_hours * 3600 

    invite = await inter.channel.create_invite(max_age=max_age_seconds, max_uses=max_uses)
    await inter.response.send_message(f"Ссылка-приглашение на сервер: {invite.url}")


if __name__ == '__main__':
    bot.run('MTI1NDg0NjU0NzU2MTAyNTY1OQ.GYXEvP.cNogCk7nPPFU7UUXLF5M03GwSManji807OZXgk')


    