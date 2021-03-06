from .models import Genotypes, QR_Code
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
            # Allow of comment and experiment to be blank
            if len(fields) < 7 or len(fields) > 9:
                issues += 1
                info = ("The number of fields for this line is incorrect " +
                        "sure you have nine columns of data and that it is " +
                        "tab seperated. You can have 7 columns with " +
                        "experiment and comments blank")
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

    # take off flie path and just the base name with suffix
    pass_file_name = pass_file.name.split("/")[-1]
    fail_file_name = fail_file.name.split("/")[-1]
    fail_file.close()
    pass_file.close()
    print(total)

    if issues == 0:
        # go back through file to add to DB instead of partial adds
        file = open(pass_file, 'r')
        for line in file:
            line = line.decode().strip()
            if line.startswith("parent"):
                continue
            else:
                fields = line.split("\t")
                # Check if the m and f parent row combo already exists in DB
                try:
                    QueryGeno = Genotypes.objects.get(parent_f_row__iexact=fields[0],
                                                      parent_m_row__iexact=fields[1],
                                                      )
                    QueryGeno.seed_count += int(fields[5])
                    QueryGeno.save()

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
        pass_file.close()

    return(pass_file_name, fail_file_name, issues)


def subtractions_download(data):
    # create log files, note that they are not temp files
    # we use the name temp file to generate the random 6 character file name
    pass_file = tempfile.NamedTemporaryFile(suffix="_log.txt",
                                            prefix="withdraaw_pass_",
                                            dir=settings.MEDIA_ROOT+'/logs',
                                            mode='w',
                                            delete=False)
    fail_file = tempfile.NamedTemporaryFile(suffix="__log.txt",
                                            prefix="withdraw_fail_",
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
            if len(fields) >= 7 and len(fields) <= 9:
                issues += 1
                info = ("The number of fields for this line is incorrect. " +
                        "sure you have nine columns of data, " +
                        "and that it is tab seperated")
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
                info = ('Seed count number must be positive to withdraw')
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
                QueryGeno.seed_count -= int(fields[5])
                if QueryGeno.seed_count < 0:
                    issues += 1
                    info = ("WARNING: " +
                            fields[5] +
                            " does not have enough seed. " +
                            "Stock would have been set at " +
                            str(QueryGeno.seed_count) +
                            " seeds from DB, but it is a negative number. " +
                            "You don't have enough seed, " +
                            "check your seed stocks")
                    print(line, info, sep='\t', file=fail_file)

                else:
                    info = ("Removed " + fields[5]+" seeds from DB they're " +
                            str(QueryGeno.seed_count) +
                            "remaining")
                    print(line, info, sep='\t', file=pass_file)

            # If the query does not exist, make a new one
            except Genotypes.DoesNotExist:
                info = ("lines " +
                        fields[0] +
                        ' ' +
                        fields[1] +
                        " don't exist in DB, please make sure you spelled " +
                        " them correctly")
                print(line, info, sep='\t', file=fail_file,)

    # take off flie path and just the base name with suffix
    pass_file_name = pass_file.name.split("/")[-1]
    fail_file_name = fail_file.name.split("/")[-1]
    fail_file.close()
    pass_file.close()
    print(total)

    if issues == 0:
        # go back through file to add to DB instead of partial adds
        file = open(pass_file, 'r')
        for line in file:
            line = line.decode().strip()
            if line.startswith("parent"):
                continue
            else:
                fields = line.split("\t")
            QueryGeno = Genotypes.objects.get(parent_f_row__iexact=fields[0],
                                              parent_m_row__iexact=fields[1],
                                              )
            QueryGeno.seed_count -= int(fields[5])
            QueryGeno.save()
        pass_file.close()

    return(pass_file_name, fail_file_name, issues)


def QR_code_check(data):
    has_QR_file = tempfile.NamedTemporaryFile(suffix="_log.txt",
                                              prefix="withdraw_pass_",
                                              dir=settings.MEDIA_ROOT+'/logs',
                                              mode='w',
                                              delete=False)
    no_QR_file = tempfile.NamedTemporaryFile(suffix="__log.txt",
                                             prefix="withdraw_fail_",
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
            if len(fields) != 7:
                issues += 1
                info = ("The number of fields for this line is incorrect. " +
                        "sure you have nine columns of data, " +
                        "and that it is tab seperated")
                print(line, info, sep='\t', file=no_QR_file)
                continue
            try:
                QueryQR = QR_Code.objects.get(parent_f_row__iexact=fields[0],
                                              parent_m_row__iexact=fields[1],
                                              )
                info = ("Barcode already existed for " +
                        fields[0] +
                        "_" +
                        fields[1] +
                        "combination"
                        )
                print(QueryQR, info, sep='\t', file=has_QR_file)

            # If the query does not exist, make a new one
            except QR_Code.DoesNotExist:
                NewQRcd = QR_Code(parent_f_row=fields[0],
                                  parent_m_row=fields[1],
                                  parent_f_geno=fields[2],
                                  parent_m_geno=fields[3],
                                  genotype=fields[4],
                                  plot=fields[5],
                                  ranges=fields[6],
                                  qr_code="{% qr_from_text " +
                                          fields[0] +
                                          "_" +
                                          fields[1] +
                                          " size=\"T\" %}",
                                  )
                NewQRcd.save()

                info = ("Added " + fields[0]+' '+fields[1]+" QR to DB")
                print(NewQRcd, info, sep='\t', file=has_QR_file,)

    # take off file path and just the base name with suffix
    pass_file_name = has_QR_file.name.split("/")[-1]
    fail_file_name = no_QR_file.name.split("/")[-1]
    no_QR_file.close()
    has_QR_file.close()
    print(total)

    return(pass_file_name, fail_file_name, issues)
