import bs4 as bs
sr = '<select size="4" name="lstLeft" id="lstLeft" class="bld" style="font-weight:bold;height:200px;width:100%;">\n\t<option value="1">B.E. Chemical (Pilani Campus)</option>\n\t<option value="2">B.E. Chemical (Goa Campus)</option>\n\t<option value="3">B.E. Chemical (Hyderabad Campus)</option>\n\t<option value="4">B.E. Civil (Pilani Campus)</option>\n\t<option value="5">B.E. Civil (Hyderabad Campus)</option>\n\t<option value="6">B.E. Electrical &amp; Electronics (Pilani Campus)</option>\n\t<option value="7">B.E. Electrical &amp; Electronics (Goa Campus)</option>\n\t<option value="8">B.E. Electrical &amp; Electronics (Hyderabad Campus)</option>\n\t<option value="9">B.E. Mechanical (Pilani Campus)</option>\n\t<option value="10">B.E. Mechanical (Goa Campus)</option>\n\t<option value="11">B.E. Mechanical (Hyderabad Campus)</option>\n\t<option value="12">B.E. Computer Science (Pilani Campus)</option>\n\t<option value="13">B.E. Computer Science (Goa Campus)</option>\n\t<option value="14">B.E. Computer Science (Hyderabad Campus)</option>\n\t<option value="15">B.E. Electronics &amp; Instrumentation (Pilani Campus)</option>\n\t<option value="16">B.E. Electronics &amp; Instrumentation (Goa Campus)</option>\n\t<option value="17">B.E. Electronics &amp; Instrumentation (Hyderabad Campus)</option>\n\t<option value="18">B.E. Electronics &amp; Communication (Pilani Campus)</option>\n\t<option value="19">B.E. Electronics &amp; Communication (Goa Campus)</option>\n\t<option value="20">B.E. Electronics &amp; Communication (Hyderabad Campus)</option>\n\t<option value="21">B.E. Manufacturing (Pilani Campus)</option>\n\t<option value="22">M.Sc. Biological Sciences (Pilani Campus)</option>\n\t<option value="23">M.Sc. Biological Sciences (Goa Campus)</option>\n\t<option value="24">M.Sc. Biological Sciences (Hyderabad Campus)</option>\n\t<option value="25">M.Sc. Chemistry (Pilani Campus)</option>\n\t<option value="26">M.Sc. Chemistry (Goa Campus)</option>\n\t<option value="27">M.Sc. Chemistry (Hyderabad Campus)</option>\n\t<option value="28">M.Sc. Economics (Pilani Campus)</option>\n\t<option value="29">M.Sc. Economics (Goa Campus)</option>\n\t<option value="30">M.Sc. Economics (Hyderabad Campus)</option>\n\t<option value="31">M.Sc. Mathematics (Pilani Campus)</option>\n\t<option value="32">M.Sc. Mathematics (Goa Campus)</option>\n\t<option value="33">M.Sc. Mathematics (Hyderabad Campus)</option>\n\t<option value="34">M.Sc. Physics (Pilani Campus)</option>\n\t<option value="35">M.Sc. Physics (Goa Campus)</option>\n\t<option value="36">M.Sc. Physics (Hyderabad Campus)</option>\n\n</select>'
soup = bs.BeautifulSoup(sr, 'lxml')
a= soup.find_all('option')
print(len(a))
l = []
for i in a:
    l.append(i.get_text())
l2 = []
for i in l:
    if 'B.E.' in i:
        l2.append(i)
l_p =[]
l_g = []
l_h = []
for i in l2:
    if "Pilani Campus" in i:
        l_p.append(i)
    elif 'Goa Campus' in i:
        l_g.append(i)
    elif 'Hyderabad Campus' in i:
        l_h.append(i)