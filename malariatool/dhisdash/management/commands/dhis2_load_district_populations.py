# Data Source: http://unstats.un.org/unsd/demographic/sources/census/wphc/Uganda/UGA-2014-11.pdf
from django.core.management import BaseCommand

from dhisdash.models import District


class Command(BaseCommand):
    help = 'Load the district populations'

    def add_arguments(self, parser):
        parser.add_argument('source_file', nargs='+')

    def handle(self, *args, **options):
        source_file = options['source_file'][0]
        lines = open(source_file, 'r').readlines()

        total = 0
        for line in lines:
            split_line = line.strip().split(" ")
            size = int(split_line[-1].replace(",", ""))
            name = split_line[0]
            print ">> %s - %s" % (name, size)

            districts = District.objects.filter(name__icontains=name)
            if len(districts) > 0:
                print "(Match Found)"
                try:
                    first_match = districts[0]
                    first_match.population = size
                    first_match.save()

                    print "(Saved)"
                except Exception, e:
                    print e.message

            total += size

        print "Total: %s" % total