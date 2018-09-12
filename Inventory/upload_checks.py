from .models import Genotypes
import tempfile
from django.conf import settings


# This is to start and check if uploads with pass when adding inventory
def CheckInt(num):
    try: 
        int(num)
        return True
    except ValueError:
        return False


def additions_upload(data):
    # create log files, note that they are not temp files
    # we use the name temp file to generate the random 6 character file name
    pass_file = tempfile.NamedTemporaryFile(suffix="_log.txt",
                                            prefix="addition_pass_",
                                            dir=settings.MEDIA_ROOT+'/logs',
                                            mode='w',
                                            delete=False)
    fail_file = tempfile.NamedTemporaryFile(suffix="__log.txt",
                                            prefix="addition_fail_",
                                            dir=settings.MEDIA_ROOT+'/logs',
                                            mode='w',
                                            delete=False)
    issues = 0
    total = 0
    for line in data:
        total += 1
        line = line.decode().strip()

        # check to see if there is header line or skip
        if line.startswith("parent"):
            continue
        else:
            fields = line.split("\t")
            if len(fields) != 9:
                issues += 1
                info = ('The number of fields for this line is incorrect sure you have nine columns of data and that it is tab seperated')
                print(line, info, sep='\t', file=fail_file)
                continue

            # make sure seed cound is an int
            if CheckInt(fields[5]) is False:
                issues += 1
                info = ('Seed count column must have a number in it')
                print(line, info, sep='\t', file=fail_file)
                continue

            # make sure seed count is positive
            if int(fields[5]) < 0:
                issues += 1
                info = ('Seed count number must be positive to add')
                print(line, info, sep='\t', file=fail_file)
                continue

            # Check true/false field
            if (fields[6].startswith("T")) or (fields[6].startswith("t")):
                fields[6] = True
            else:
                fields[6] = False

            # Check if the m and f parent row combo already exists in DB
            try:
                QueryGeno = Genotypes.objects.get(parent_f_row__iexact=fields[0],
                                                  parent_m_row__iexact=fields[1],
                                                  )
                QueryGeno.seed_count += int(fields[5])
                QueryGeno.save()
                info = ("Added " + fields[5]+" seeds to DB")
                print(line, info, sep='\t', file=pass_file)

            # If the query does not exist, make a new one
            except Genotypes.DoesNotExist:
                NewGeno = Genotypes(parent_f_row=fields[0],
                                    parent_m_row=fields[1],
                                    parent_f_geno=fields[2],
                                    parent_m_geno=fields[3],
                                    genotype=fields[4],
                                    seed_count=fields[5],
                                    actual_count=fields[6],
                                    experiment=fields[7],
                                    comments=fields[8],
                                    )
                NewGeno.save()

                info = ("Added " + fields[0]+' '+fields[1]+" harvest to DB")
                print(line, info, sep='\t', file=pass_file,)

    # take off flie path and just the base name with suffix
    pass_file_name = pass_file.name.split("/")[-1]
    fail_file_name = fail_file.name.split("/")[-1]
    fail_file.close()
    pass_file.close()
    print (total)

    return(pass_file_name, fail_file_name, issues)
