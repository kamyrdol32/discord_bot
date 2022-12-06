import datetime

import discord
from discord.ext import commands, tasks
from bs4 import BeautifulSoup
import requests

import db

scrapper_channel_id = int(1047609196159455282)
URL_BULLDOGJON = "https://bulldogjob.pl/companies/jobs/s/city,Remote,Krakow/role,support,backend,frontend,fullstack,administrator/experienceLevel,junior/page,"
URL_NOFLUFFJOBS = "https://nofluffjobs.com/pl/praca-zdalna/backend?criteria=city%3Dkrakow%20category%3Dfrontend,fullstack,devops,gaming,it-administrator,product-management,project-manager%20seniority%3Dtrainee,junior%20requirement%3DPython&page="
class JobScrapper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bulldogjob.start()
        self.nofluffjobs.start()

    async def cog_load(self):
        print(f"{self.__class__.__name__} loaded!")

    async def cog_unload(self):
        print(f"{self.__class__.__name__} unloaded!")


    @tasks.loop(minutes=15)
    async def bulldogjob(self):

        # Loop through all pages
        for i in range(1, 10):
            page = requests.get(URL_BULLDOGJON + str(i))
            soup = BeautifulSoup(page.content, 'html.parser')
            results = soup.find(id='__next')
            job_elems = results.find_all("div", ["py-6", "px-8"])

            for job_elem in job_elems:

                # Loop through all jobs
                try:

                    # Get data
                    Company = job_elem.find("p", class_="text-sm md:text-xxs md:text-center my-2 font-medium text-gray-300")
                    if Company is not None:
                        Company = Company.text.strip()

                    Name = job_elem.find("h3", class_="text-c28 font-medium mb-3 w-full md:hidden")
                    if Name is not None:
                        Name = Name.text.strip()

                    Salary = job_elem.find("div", class_="text-c28 font-medium md:py-1 inline-block")
                    if Salary is not None:
                        Salary = Salary.text.strip()

                    Contract = job_elem.find("p", class_="font-medium mb-4 md:my-4 flex flex-wrap items-center")
                    if Contract is not None:
                        Contract = Contract.text.strip()

                    Link = job_elem.find("a", class_="absolute top-0 left-0 w-full h-full")
                    Link = Link['href']

                    if Link is not None:
                        ID = Link.split('/')[-1]
                        ID = ID.split('-')[0]

                    if Contract == "Kontrakt B2BUmowa o pracę":
                        Contract = "Kontrakt B2B | Umowa o pracę"
                    elif Contract == "Umowa o pracęInna forma zatrudnienia":
                        Contract = "Umowa o pracę | Inna forma zatrudnienia"
                    elif Contract == "Kontrakt B2BUmowa o pracęInna forma zatrudnienia":
                        Contract = "Kontrakt B2B | Umowa o pracę | Inna forma zatrudnienia"

                    # Check if job is already in database
                    stmt = db.select(db.Job).where(db.Job.Job_ID == "B" + str(ID))
                    result = db.session.execute(stmt).first()
                    if result:
                        print("[BullDogJob] Job already in database - " + Name)
                        continue
                    else:
                        print("[BullDogJob] New job - " + Name)

                    # Add to database
                    Job = db.Job(Job_ID="B" + str(ID), Company=Company, Name=Name, Salary=Salary, Contract=Contract, Link=Link)
                    db.session.add(Job)
                    db.session.commit()
                    await self.send_message(str(ID), str(Company), str(Name), str(Salary), str(Contract), str(Link), "BulldogJob.pl", [255, 179, 0])

                except Exception as error:
                    print("[ERROR] bulldogjob - " + str(error))


    @tasks.loop(minutes=15)
    async def nofluffjobs(self):

        # Loop through all pages
        for i in range(1, 10):
            page = requests.get(URL_NOFLUFFJOBS + str(i))
            soup = BeautifulSoup(page.content, 'html.parser')
            results = soup.find("div", class_="mt-3 mt-md-5 mb-20 ng-star-inserted")
            job_elems = results.find_all("a", ["posting-list-item", "posting-list-item--backend"])

            # Loop through all jobs
            for job_elem in job_elems:

                try:

                    # Get data
                    Company = job_elem.find("span", class_="posting-title__company")
                    if Company is not None:
                        Company = Company.text.strip()

                    Name = job_elem.find("h3", class_="posting-title__position")
                    if Name is not None:
                        Name = Name.text.strip()

                    Salary = job_elem.find("span", class_="salary")
                    if Salary is not None:
                        Salary = Salary.text.strip()

                    Contract = "Brak informacji"

                    Link = job_elem
                    Link = "https://nofluffjobs.com" + str(Link['href'])
                    if Link is not None:
                        ID = Link.split('-')[-1]

                    # Check if job is already in database
                    stmt = db.select(db.Job).where(db.Job.Job_ID == "N" + str(ID))
                    result = db.session.execute(stmt).first()
                    if result:
                        print("[NoFluffJons] Job already in database - " + Name)
                        continue
                    else:
                        print("[NoFluffJons] New job - " + Name)

                    # Add to database
                    Job = db.Job(Job_ID="N" + str(ID), Company=Company, Name=Name, Salary=Salary, Contract=Contract, Link=Link)
                    db.session.add(Job)
                    db.session.commit()
                    await self.send_message(str(ID), str(Company), str(Name), str(Salary), str(Contract), str(Link), "NoFluffJobs.com", [255, 179, 0])

                except Exception as error:
                    print("[ERROR] nofluffjobs - " + str(error))


    async def send_message(self, ID, Company, Name, Salary, Contract, Link, Site, Color):

        try:

            # Create embed
            embed = discord.Embed(title="**" + Name + "**", color=discord.Colour.from_rgb(Color[0], Color[1], Color[2]))
            embed.add_field(name="**Firma**:", value=Company, inline=False)
            embed.add_field(name="**Wynagrodzenie**:", value=Salary, inline=True)
            embed.add_field(name="**Umowa**:", value=Contract, inline=True)
            embed.set_footer(text=str(Site) + " | " + str(ID))
            embed.timestamp = datetime.datetime.utcnow()

            # Create view
            url_view = discord.ui.View()
            url_view.add_item(discord.ui.Button(label='LINK', style=discord.ButtonStyle.url, url=Link))

            # Send message
            scrapper_channel = self.bot.get_channel(int(scrapper_channel_id))
            await scrapper_channel.send(embed=embed, view=url_view)

        except Exception as error:
            print("[ERROR] send_message - " + str(error))


    @bulldogjob.before_loop
    @nofluffjobs.before_loop
    async def before_scrapper(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(JobScrapper(bot=bot))