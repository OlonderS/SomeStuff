using DDD.CarRental.Core.DomainModelLayer.Models;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Numerics;
using System.Text;
using System.Threading.Tasks;

namespace DDD.CarRental.Core.InfrastructureLayer.EF.EntityConfigurations
{
    public class RentalConfiguration : IEntityTypeConfiguration<Rental>
    {
        public void Configure(EntityTypeBuilder<Rental> RentalConfiguration)
        {
            RentalConfiguration.HasKey(r => r.Id);

            RentalConfiguration.Property(r => r.Id).ValueGeneratedNever();

            // wykluczenie DomainsEvents z modelu relacyjnego - nie ma potrzeby zapisywania w bazie zdarzeń domenowych
            RentalConfiguration.Ignore(r => r.DomainEvents);

            RentalConfiguration.Property<long>("DriverId").IsRequired();

            // ustawienie związku 1:N pomiędzy tabelami Driver i Rental
            RentalConfiguration.HasOne<Driver>()
                .WithMany()
                .IsRequired(false)
                .HasForeignKey("DriverId");

            // ustawienie obowiązkowości klucza obcego do tabeli Car
            RentalConfiguration.Property<long>("CarId").IsRequired();

            // ustawienie związku 1:N pomiędzy tabelami  Car  i Rental
            RentalConfiguration.HasOne<Car>()
                .WithMany()
                .IsRequired(false)
                .HasForeignKey("CarId");
        }
    }
}
