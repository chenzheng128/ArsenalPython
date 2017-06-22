#!/usr/bin/perl

sub time_stamp {
  my ($d,$t);
  my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);

        $year += 1900;
        $mon++;
        $d = sprintf("%4d-%2.2d-%2.2d",$year,$mon,$mday);
        $t = sprintf("%2.2d-%2.2d-%2.2d",$hour,$min,$sec);      
	return("$d\_$t");
}



########## Moving Files ##########
$ts = &time_stamp();
mkdir("res-$ts", 0755) || die "Cannot mkdir res-$ts: $!";
system("cp ./vs*.png ./res-$ts");

########## Creating html_heterogeneous.html File ##########
$path = "./res-$ts/html_heterogeneous.html";
open(SINK, "> $path") or die "Couldn't open $path for writing: $!\n";

print SINK "<html>\n";
print SINK "<head>\n";
print SINK "<title>TCP Evaluation Suite Simulation Results: Performance Heterogeneous<title>\n";
print SINK "</head>\n";
print SINK "<body>\n";
print SINK "<h2>TCP Evaluation Suite Simulation Results: Performance Heterogeneous</h2>\n";
print SINK "<ul>\n";
print SINK "<li><b>Performance Heterogeneous</b></li>\n";
print SINK "<li><a href=\"html_homogeneous.html\">Performance Homogeneous</a></li>\n";
print SINK "<li><a href=\"html_flowdynamics.html\">Flow Dynamics</a></li>\n";
print SINK "<li><a href=\"html_usage.html\">Network and Core Usage</a></li>\n";
print SINK "</ul>\n";
print SINK "<table>\n";
print SINK "<tr>\n";
print SINK "<td><img src=\"vsreno-fcompb1.png\"/></td>\n";
print SINK "<td><img src=\"vsreno-fcompb2.png\"/></td>\n";
print SINK "</tr>\n";
print SINK "<tr>\n";
print SINK "<td><img src=\"vsreno-fcomph1.png\"/></td>\n";
print SINK "<td><img src=\"vsreno-fcomph2.png\"/></td>\n";
print SINK "</tr>\n";
print SINK "<tr>\n";
print SINK "<td><img src=\"vsreno-fcompr1.png\"/></td>\n";
print SINK "<td><img src=\"vsreno-fcompr2.png\"/></td>\n";
print SINK "</tr>\n";
print SINK "</table>\n";
print SINK "</body>\n";
print SINK "</html>";

close(SINK);
########## Finished Creating html_heterogeneous2.html File ##########
######################################################################

########## Creating tex_heterogeneous.pdf File ##########
$path = "./res-$ts/tex_heterogeneous.tex";
open(SINK, "> $path") or die "Couldn't open $path for writing: $!\n";

print SINK "\\documentclass{article}\n";
print SINK "\\usepackage{fullpage,graphicx}\n";
print SINK "\\usepackage\[top=0in\]{geometry}\n";
print SINK "\\begin{document}\n";
print SINK "\\title{TCP Evaluation Suite Simulation Results: Performance Heterogeneous}\n";
print SINK "\\maketitle\n";
print SINK "\\begin{figure}[htbp]\n";
print SINK "\\centering\n";
print SINK "\\includegraphics[scale=0.5]{vsreno-fcompb1.png}%\n";
print SINK "\\includegraphics[scale=0.5]{vsreno-fcompb2.png}\n";
print SINK "\\includegraphics[scale=0.5]{vsreno-fcomph1.png}%\n";
print SINK "\\includegraphics[scale=0.5]{vsreno-fcomph2.png}\n";
print SINK "\\includegraphics[scale=0.5]{vsreno-fcompr1.png}%\n";
print SINK "\\includegraphics[scale=0.5]{vsreno-fcompr2.png}\n";
print SINK "\\end{figure}\n";
print SINK "\\end{document}";

close(SINK);
system("pdflatex -output-directory=./res-$ts ./res-$ts/tex_heterogeneous.tex");
########## Finished Creating tex_heterogeneous.pdf File ##########
######################################################################

########## Creating html_homogeneous.html File ##########
$path = "./res-$ts/html_homogeneous.html";
open(SINK, "> $path") or die "Couldn't open $path for writing: $!\n";

print SINK "<html>\n";
print SINK "<head>\n";
print SINK "<title>TCP Evaluation Suite Simulation Results: Performance Homogeneous<title>\n";
print SINK "</head>\n";
print SINK "<body>\n";
print SINK "<h2>TCP Evaluation Suite Simulation Results: Performance Homogeneous</h2>\n";
print SINK "<ul>\n";
print SINK "<li><a href=\"html_heterogeneous.html\">Performance Heterogeneous</a></li>\n";
print SINK "<li><b>Performance Homogeneous</b></li>\n";
print SINK "<li><a href=\"html_flowdynamics.html\">Flow Dynamics</a></li>\n";
print SINK "<li><a href=\"html_usage.html\">Network and Core Usage</a></li>\n";
print SINK "</ul>\n";
print SINK "<table>\n";
print SINK "<tr>\n";
print SINK "<td><img src=\"vshs-favgb.png\"/></td>\n";
print SINK "<td><img src=\"vshs-fcompb.png\"/></td>\n";
print SINK "</tr>\n";
print SINK "<tr>\n";
print SINK "<td><img src=\"vshs-favgh.png\"/></td>\n";
print SINK "<td><img src=\"vshs-fcomph.png\"/></td>\n";
print SINK "</tr>\n";
print SINK "<tr>\n";
print SINK "<td><img src=\"vshs-favgr.png\"/></td>\n";
print SINK "<td><img src=\"vshs-fcompr.png\"/></td>\n";
print SINK "</tr>\n";
print SINK "</table>\n";
print SINK "</body>\n";
print SINK "</html>";

close(SINK);
########## Finished Creating html_homogeneous2.html File ##########
######################################################################

########## Creating tex_homogeneous.pdf File ##########
$path = "./res-$ts/tex_homogeneous.tex";
open(SINK, "> $path") or die "Couldn't open $path for writing: $!\n";

print SINK "\\documentclass{article}\n";
print SINK "\\usepackage{fullpage,graphicx}\n";
print SINK "\\usepackage\[top=0in\]{geometry}\n";
print SINK "\\begin{document}\n";
print SINK "\\title{TCP Evaluation Suite Simulation Results: Performance Homogeneous}\n";
print SINK "\\maketitle\n";
print SINK "\\begin{figure}[htbp]\n";
print SINK "\\centering\n";
print SINK "\\includegraphics[scale=0.5]{vshs-favgb.png}%\n";
print SINK "\\includegraphics[scale=0.5]{vshs-fcompb.png}\n";
print SINK "\\includegraphics[scale=0.5]{vshs-favgh.png}%\n";
print SINK "\\includegraphics[scale=0.5]{vshs-fcomph.png}\n";
print SINK "\\includegraphics[scale=0.5]{vshs-favgr.png}%\n";
print SINK "\\includegraphics[scale=0.5]{vshs-fcompr.png}\n";
print SINK "\\end{figure}\n";
print SINK "\\end{document}";

close(SINK);
system("pdflatex -output-directory=./res-$ts ./res-$ts/tex_homogeneous.tex");
########## Finished Creating tex_homogeneous.pdf File ##########
######################################################################

########## Creating html_flowdynamics.html File ##########
$path = "./res-$ts/html_flowdynamics.html";
open(SINK, "> $path") or die "Couldn't open $path for writing: $!\n";

print SINK "<html>\n";
print SINK "<head>\n";
print SINK "<title>TCP Evaluation Suite Simulation Results: Flow Dynamics<title>\n";
print SINK "</head>\n";
print SINK "<body>\n";
print SINK "<h2>TCP Evaluation Suite Simulation Results: Flow Dynamics</h2>\n";
print SINK "<ul>\n";
print SINK "<li><a href=\"html_heterogeneous.html\">Performance Heterogeneous</a></li>\n";
print SINK "<li><a href=\"html_homogeneous.html\">Performance Homogeneous</a></li>\n";
print SINK "<li><b>Flow Dynamics</b></li>\n";
print SINK "<li><a href=\"html_usage.html\">Network and Core Usage</a></li>\n";
print SINK "</ul>\n";
print SINK "</body>\n";
print SINK "</html>";

close(SINK);
########## Finished Creating html_homogeneous2.html File ##########
######################################################################

########## Creating html_usage.html File ##########
$path = "./res-$ts/html_usage.html";
open(SINK, "> $path") or die "Couldn't open $path for writing: $!\n";

print SINK "<html>\n";
print SINK "<head>\n";
print SINK "<title>TCP Evaluation Suite Simulation Results: Network and Core Usage<title>\n";
print SINK "</head>\n";
print SINK "<body>\n";
print SINK "<h2>TCP Evaluation Suite Simulation Results: Network and Core Usage</h2>\n";
print SINK "<ul>\n";
print SINK "<li><a href=\"html_heterogeneous.html\">Performance Heterogeneous</a></li>\n";
print SINK "<li><a href=\"html_homogeneous.html\">Performance Homogeneous</a></li>\n";
print SINK "<li><a href=\"html_flowdynamics.html\">Flow Dynamics</a></li>\n";
print SINK "<li><b>Network and Core Usage</b></li>\n";
print SINK "</ul>\n";
print SINK "</body>\n";
print SINK "</html>";

close(SINK);
########## Finished Creating html_usage.html File ##########
######################################################################






