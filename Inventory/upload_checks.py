from .models import Genotypes
import tempfile
from django.conf import settings


# This is to start and check if uploads with pass when adding inventory
def additions_upload(data):
    # create log files, note that they are not temp files
    # we use the name temp file to generate the random 6 character file name
    pass_file = tempfile.NamedTemporaryFile(suffix="_log.txt",
                                            prefix="pass_",
                                            dir=settings.MEDIA_ROOT+'/logs',
                                            mode='w',
                                            delete=False)
    fail_file = tempfile.NamedTemporaryFile(suffix="__log.txt",
                                            prefix="fail_",
                                            dir=settings.MEDIA_ROOT+'/logs',
                                            mode='w',
                                            delete=False)
    issues = 0

    for line in data:
        line = line.decode().strip()
        # check to see if there is header line or skip
        if line.startswith("parent"):
            continue
        else:
            fields = line.split("\t")
            if len(fields) != 9:
                raise ValueError('The number of feild for this line is incorrect sure you have nine columns of data and that it is tab seperated')
            if (fields[6].startswith("T")) or (fields[6].startswith("t")):
                fields[6] = True
            else:
                fields[6] = False

            try:
                QueryGeno = Genotypes.objects.get(parent_f_row__iexact=fields[0],
                                                  parent_m_row__iexact=fields[1],
                                                  )
                QueryGeno.seed_count += int(fields[5])
                QueryGeno.save()
                # issues += 1
                # print(QueryGeno.parent_f_row,
                #       ' ',
                #       QueryGeno.parent_m_row,
                #       'alread exists',)
                res = ("Added " + fields[5]+" seeds to DB")
                print(line, res, file=pass_file, sep='\t')


                # QueryGeno.seed_count += fields[5]

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
    pass_file_name = pass_file.name.split("/")[-1]
    fail_file_name = fail_file.name.split("/")[-1]
    fail_file.close()
    pass_file.close()

    return(pass_file_name, fail_file_name, issues)
