using DDD.CarRental.Core.DomainModelLayer.Models;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DDD.CarRental.Core.InfrastructureLayer.EF.EntityConfigurations
{
    public class CarConfiguration : IEntityTypeConfiguration<Car>
    {
        public void Configure(EntityTypeBuilder<Car> carConfiguaion)
        {
            // ustawianie klucza głównego
            carConfiguaion.HasKey(r => r.Id);

            // klucz tabeli nie będzie generowany przez EF
            carConfiguaion.Property(r => r.Id).ValueGeneratedNever();

            // rejestracja  ma być unikalna
            carConfiguaion.HasIndex(c => c.RegistrationNumber).IsUnique();

            // wykluczenie DomainsEvents z modelu relacyjnego
            carConfiguaion.Ignore(c => c.DomainEvents);

          
        }
    }
}
