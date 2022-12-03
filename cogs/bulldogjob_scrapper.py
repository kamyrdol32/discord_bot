from discord.ext import commands, tasks
from bs4 import BeautifulSoup
import requests

import db

scrapper_channel_id = 1047609196159455282
URL = "https://bulldogjob.pl/companies/jobs/s/city,Remote,Krakow/role,support,backend,frontend,fullstack,administrator/experienceLevel,junior"


class BullDogJob_Scrapper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.scrapper.start()

    async def cog_load(self):
        print(f"{self.__class__.__name__} loaded!")

    async def cog_unload(self):
        print(f"{self.__class__.__name__} unloaded!")


    @tasks.loop(hours=1)
    async def scrapper(self):

        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find(id='__next')
        job_elems = results.find_all("div", ["py-6", "px-8"])

        print("####################")

        for job_elem in job_elems:

            try:

                Company = job_elem.find("p", class_="text-sm md:text-xxs md:text-center my-2 font-medium text-gray-300")
                if Company is not None:
                    Company = Company.text.strip()
                    # print(Company)

                Name = job_elem.find("h3", class_="text-c28 font-medium mb-3 w-full md:hidden")
                if Name is not None:
                    Name = Name.text.strip()
                    # print(Name)

                Salary = job_elem.find("div", class_="text-c28 font-medium md:py-1 inline-block")
                if Salary is not None:
                    Salary = Salary.text.strip()
                    # print(Salary)

                Contract = job_elem.find("p", class_="font-medium mb-4 md:my-4 flex flex-wrap items-center")
                if Contract is not None:
                    Contract = Contract.text.strip()
                    # print(Contract)

                Link = job_elem.find("a", class_="absolute top-0 left-0 w-full h-full")
                # if Link is not None:
                    # print(Link['href'])

                # Check if job is already in database
                stmt = db.select(db.Job).where(db.Job.Link == Link['href'])
                result = db.session.execute(stmt).first()
                if result:
                    print("Job already in database - " + Name)
                    continue
                else:
                    print("New job - " + Name)

                # Add to database
                Job = db.Job(Company=Company, Name=Name, Salary=Salary, Contract=Contract, Link=Link['href'])
                db.session.add(Job)
                db.session.commit()

                # Send message
                scrapper_channel = self.bot.get_channel(id(scrapper_channel_id))
                await scrapper_channel.send(f"New job - {Name} - {Link['href']}")
                print(scrapper_channel)

            except Exception as error:
                print(error)

async def setup(bot):
    await bot.add_cog(BullDogJob_Scrapper(bot=bot))