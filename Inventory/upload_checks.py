from .models import Genotypes


# This is to start and check if uploads with pass when adding inventory
def additions_upload(data):
    for line in data:
        line = line.decode().strip()
        # check to see if there is header line or skip
        if line.startswith("parent"):
            continue
        else:
            fields = line.split("\t")
            if len(fields) != 9:
                raise ValueError('The number of feild for this line is please make sure you have nine columns of data and that it is tab seperated')
            if (fields[6].startswith("T")) or (fields[6].startswith("t")):
                fields[6] = True
            else:
                fields[6] = False

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


# from .models import Genotypes


# # This is to start and check if uploads with pass when adding inventory
# def additions_upload(data):
#     for line in data:
#         line = line.decode().strip()
#         # check to see if there is header line or skip
#         if line.startswith("parent"):
#             continue
#         else:
#             fields = line.split("\t")
#             if len(fields) != 9:
#                 raise ValueError('The number of feild for this line is incorrect sure you have nine columns of data and that it is tab seperated')
#             if (fields[6].startswith("T")) or (fields[6].startswith("t")):
#                 fields[6] = True
#             else:
#                 fields[6] = False


#             Geno, Exists = Genotypes.objects.get(parent_f_row=fields[0],
#                                                  parent_m_row=fields[1],
#                                                  )
#             if Exists is True:
#                 print(fields[0], " alread exists")
#                 print(Geno)

#             else:
#                 NewGeno = Genotypes(parent_f_row=fields[0],
#                                     parent_m_row=fields[1],
#                                     parent_f_geno=fields[2],
#                                     parent_m_geno=fields[3],
#                                     genotype=fields[4],
#                                     seed_count=fields[5],
#                                     actual_count=fields[6],
#                                     experiment=fields[7],
#                                     comments=fields[8],
#                                     )
#                 NewGeno.save()
