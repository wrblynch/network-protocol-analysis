close all;

% Automating plotting
str1 = "data/";
stri = ["interarrivalTime_BitTorrent.csv", "interarrivalTime_FTP.csv", "interarrivalTime_HTTP.csv", "interarrivalTime_VoIP.csv"];
strp = ["payload_BitTorrent.csv", "payload_FTP.csv", "payload_HTTP.csv", "payload_VoIP.csv"];

title_str = ["BitTorrent", "FTP", "HTTP", "VoIP"];
title_str2 = ["Interarrival Time", "Payload Size"];
title_str3 = ["CDF", "PDF"];
space = " ";

for i=1:4
    
    str_tot = strcat(str1, stri(i));
    str_tot2 = strcat(str1, strp(i));
    interarrival_times = readmatrix(str_tot);
    payload = readmatrix(str_tot2);

    y_cdf = ecdf(interarrival_times);

    figure();
    plot(y_cdf);
    tot_str = strcat(title_str(i), space, title_str2(1), space, title_str3(1));
    title(tot_str);

    figure();
    histogram(interarrival_times, 1000);
    tot_str = strcat(title_str(i), space,title_str2(1), space, title_str3(2));
    title(tot_str);

    y2_cdf = ecdf(payload);

    figure();
    plot(y2_cdf);
    tot_str = strcat(title_str(i), space,title_str2(2), space, title_str3(1));
    title(tot_str);

    figure();
    y2_pdf = histogram(payload, 1000);
    tot_str = strcat(title_str(i), space, title_str2(2), space, title_str3(2));
    title(tot_str);
end


