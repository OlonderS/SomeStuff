using Projekt_web.Models.DbModels;
using System;
using System.Collections.Generic;
using System.Data.Entity;
using System.Linq;
using System.Web;

namespace Projekt_web.Models
{
    public class DatabaseContext : DbContext
    {
        public DatabaseContext() : base("Projekt_webConnectionString") { }
        public DbSet<Book> Books { get; set; }
        public DbSet<RentedBook> RentedBooks { get; set; }
        public DbSet<Library> Libraries { get; set; }

        public System.Data.Entity.DbSet<Projekt_web.Models.DbModels.Publisher> Publishers { get; set; }

        public System.Data.Entity.DbSet<Projekt_web.Models.DbModels.User> Users { get; set; }
    }
}