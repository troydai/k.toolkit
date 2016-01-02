using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using Microsoft.DotNet.ProjectModel;
using Microsoft.DotNet.ProjectModel.Graph;
using NuGet.Frameworks;

namespace VersionAligner
{
    public class Program
    {
        public static void Main(string[] args)
        {
            if (args.Length != 1)
            {
                Console.WriteLine("usage: va [source]. make sure the projects are first restored.");
                return;
            }

            var lockfiles = Directory.GetFiles(args[0], "project.lock.json", SearchOption.AllDirectories);

            var contexts = lockfiles.Select(file => ProjectContext.Create(Path.GetDirectoryName(file), NuGetFramework.Parse("dnxcore50")));

            foreach (var context in contexts)
            {
                WriteLine($"Analyzing {context.ProjectFile.ProjectDirectory}", ConsoleColor.Cyan);

                var libraries = context.LibraryManager.GetLibraries()
                                       .Where(lib => lib.Identity.Name.IndexOf("System.") == 0);

                foreach (var lib in libraries)
                {
                    var updatable = lib.RequestedRanges.Where(req => (req.VersionRange.MinVersion != lib.Identity.Version) &&
                                                                     (File.Exists(req.SourceFilePath)));

                    updatable.ForEach(req => UpdateLine(req, lib));
                }
            }
        }

        public static void WriteLine(string content, ConsoleColor color)
        {
            var oldColor = Console.ForegroundColor;
            Console.ForegroundColor = color;
            Console.WriteLine(content);
            Console.ForegroundColor = oldColor;
        }

        public static void UpdateLine(LibraryRange range, LibraryDescription library)
        {
            var content = File.ReadAllLines(range.SourceFilePath);
            var linenumber = range.SourceLine;
            var from = range.VersionRange.OriginalString;
            var to = library.Identity.Version.ToNormalizedString();

            WriteLine($"{range.Name}\n{from} => {to}\n{range.SourceFilePath}\nline:{linenumber}\ncolumn:{range.SourceColumn}\n", ConsoleColor.Gray);

            if (content[linenumber - 1].IndexOf(from) == -1)
            {
                WriteLine($"Version {from} is not found in file {range.SourceFilePath} on line {range.SourceLine}", ConsoleColor.Red);
                return;
            }
            else
            {
                content[linenumber - 1] = content[linenumber - 1].Replace(from, to);
                File.WriteAllLines(range.SourceFilePath, content);
            }
        }
    }

    public static class EnumerableExtensions
    {
        public static void Print<T>(this IEnumerable<T> self)
        {
            foreach (var each in self)
            {
                Console.WriteLine(each);
            }
        }

        public static void Print<T, K>(this IEnumerable<T> self, Func<T, K> serializer)
        {
            foreach (var each in self)
            {
                Console.WriteLine(serializer(each).ToString());
            }
        }

        public static void ForEach<T>(this IEnumerable<T> self, Action<T> action)
        {
            foreach (var each in self)
            {
                action(each);
            }
        }
    }
}
