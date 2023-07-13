namespace Projekt_web.Migrations
{
    using System;
    using System.Data.Entity.Migrations;
    
    public partial class First : DbMigration
    {
        public override void Up()
        {
            CreateTable(
                "dbo.Books",
                c => new
                    {
                        BookId = c.Int(nullable: false, identity: true),
                        Title = c.String(nullable: false, maxLength: 20),
                        Author = c.String(),
                        Description = c.String(),
                        PublisherId = c.Int(nullable: false),
                        Category = c.Int(nullable: false),
                        Date = c.DateTime(nullable: false),
                        Available = c.Boolean(nullable: false),
                        Library_LibraryId = c.Int(),
                    })
                .PrimaryKey(t => t.BookId)
                .ForeignKey("dbo.Publishers", t => t.PublisherId, cascadeDelete: true)
                .ForeignKey("dbo.Libraries", t => t.Library_LibraryId)
                .Index(t => t.PublisherId)
                .Index(t => t.Library_LibraryId);
            
            CreateTable(
                "dbo.Publishers",
                c => new
                    {
                        PublisherId = c.Int(nullable: false, identity: true),
                        Name = c.String(nullable: false, maxLength: 20),
                    })
                .PrimaryKey(t => t.PublisherId);
            
            CreateTable(
                "dbo.Libraries",
                c => new
                    {
                        LibraryId = c.Int(nullable: false, identity: true),
                        Name = c.String(),
                    })
                .PrimaryKey(t => t.LibraryId);
            
            CreateTable(
                "dbo.Users",
                c => new
                    {
                        UserId = c.Int(nullable: false, identity: true),
                        Name = c.String(),
                        Surname = c.String(),
                        Library_LibraryId = c.Int(),
                    })
                .PrimaryKey(t => t.UserId)
                .ForeignKey("dbo.Libraries", t => t.Library_LibraryId)
                .Index(t => t.Library_LibraryId);
            
            CreateTable(
                "dbo.RentedBooks",
                c => new
                    {
                        RentedBookId = c.Int(nullable: false, identity: true),
                        BookId = c.Int(nullable: false),
                        UserId = c.Int(nullable: false),
                        RentDate = c.DateTime(nullable: false),
                        ReturnDate = c.DateTime(nullable: false),
                        Penalty = c.Int(nullable: false),
                    })
                .PrimaryKey(t => t.RentedBookId)
                .ForeignKey("dbo.Books", t => t.BookId, cascadeDelete: true)
                .ForeignKey("dbo.Users", t => t.UserId, cascadeDelete: true)
                .Index(t => t.BookId)
                .Index(t => t.UserId);
            
        }
        
        public override void Down()
        {
            DropForeignKey("dbo.Users", "Library_LibraryId", "dbo.Libraries");
            DropForeignKey("dbo.RentedBooks", "UserId", "dbo.Users");
            DropForeignKey("dbo.RentedBooks", "BookId", "dbo.Books");
            DropForeignKey("dbo.Books", "Library_LibraryId", "dbo.Libraries");
            DropForeignKey("dbo.Books", "PublisherId", "dbo.Publishers");
            DropIndex("dbo.RentedBooks", new[] { "UserId" });
            DropIndex("dbo.RentedBooks", new[] { "BookId" });
            DropIndex("dbo.Users", new[] { "Library_LibraryId" });
            DropIndex("dbo.Books", new[] { "Library_LibraryId" });
            DropIndex("dbo.Books", new[] { "PublisherId" });
            DropTable("dbo.RentedBooks");
            DropTable("dbo.Users");
            DropTable("dbo.Libraries");
            DropTable("dbo.Publishers");
            DropTable("dbo.Books");
        }
    }
}
