using DDD.CarRental.Core.DomainModelLayer.Models;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DDD.CarRental.Core.InfrastructureLayer.EF.EntityConfigurations
{
    public class CarDeliveryConfiguration : IEntityTypeConfiguration<CarDelivery>
    {
        public void Configure(EntityTypeBuilder<CarDelivery> carConfiguaion)
        {
            // ustawianie klucza głównego
            carConfiguaion.HasKey(r => r.Id);

          

            // wykluczenie DomainsEvents z modelu relacyjnego
            carConfiguaion.Ignore(c => c.DomainEvents);


        }
    }
}
