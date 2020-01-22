from __future__ import print_function

import glob
import os
import shutil
import sys
import hashlib
if os.name == 'posix' and sys.version_info[0] < 3:
    import subprocess32 as subprocess
else:
    import subprocess
import sqlite3

# path to files used to populate database <movie-cast.txt, movie-name-score.txt, movie-overview.txt>
INPUT_DATA_DIR = '/data'
# path to solution files
#SQL_SOLUTION_FILE_PATH = 'Q2.SQL.SOLN.txt'
# path for DB that will be generating during grading.  Can be the same as solution directory.
MODEL_OUT_FILE_PATH = 'Q2.OUT.SOLN.txt'
MODEL_DB_FILE_PATH = 'Q2.db'


def parse_q2sql_file(filepath):
    assert os.path.exists(filepath)

    with open(filepath, 'r', encoding="ISO-8859-1") as f:
        contents = f.read().replace('\r', '')

    parsed = contents.split('-- ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** --\n')
    parsed = map(lambda txt: filter(lambda txt_: txt_ not in ['', ' '], txt.split('\n')), parsed)
    parsed = map(lambda lst: map(lambda txt: txt.strip().casefold(), lst), parsed)

    return parsed


def parse_q2out_file(filepath):
    assert os.path.exists(filepath)

    with open(filepath, 'r') as f:
        contents = f.read()

    parsed = contents.split('~~~~~\n')
    parsed = map(lambda txt: filter(lambda txt_: txt_ != '', txt.split('\n')), parsed)
    parsed = map(lambda lst: map(lambda txt: txt.replace('"', '').casefold(), lst), parsed)

    return parsed


def load_q2db_file(filepath):
    conn = sqlite3.connect(filepath)
    cursor = conn.cursor()

    return conn, cursor


if sys.version_info >= (3, 0):
    _map = map
    _filter = filter

    def map(*args, **kwargs):
        return list(_map(*args, **kwargs))

    def filter(*args, **kwargs):
        return list(_filter(*args, **kwargs))

def evaluate():
    solution_dir = os.getcwd()
    assert os.path.isdir(solution_dir)

    points = 35.0
    comments = list()

    sql_file_path = os.path.join(solution_dir, 'Q2.SQL.txt')
    out_file_path = os.path.join(solution_dir, 'Q2.OUT.txt')
    db_file_path = os.path.join(solution_dir, 'Q2.db')
    data_dir = solution_dir+"/data"

    if not os.path.exists(data_dir): os.mkdir(data_dir)
    assert os.path.isdir(data_dir)

    # no points if Q2.SQL.txt does not exist in the solution directory
    if not os.path.exists(sql_file_path):
        points -= 36.0
        comments.append('[-35] Q2.SQL.txt not found')
        return points, '; '.join(comments)

    # copy (overwrite) data files into solution directory
    
    for input_data_file_path in glob.glob(os.path.join(INPUT_DATA_DIR, '*.csv')):
        input_data_file_name = os.path.basename(input_data_file_path)

        shutil.copyfile(
            input_data_file_path,
            os.path.join(data_dir, input_data_file_name))
    
    # run sqlite command to create Q2.db and Q2.OUT.txt
    if os.path.exists(db_file_path): os.remove(db_file_path)
    if os.path.exists(out_file_path): os.remove(out_file_path)
    try:
        error_code = subprocess.call('sqlite3 Q2.db < Q2.SQL.txt > Q2.OUT.txt',
                                     cwd=solution_dir, shell=True, timeout=120)
        # if error_code != 0:
        #     points -= 35.0
        #     comments.append('[-35] error while running command: sqlite3 Q2.db < Q2.SQL.txt > Q2.OUT.txt')
        #     return points, '; '.join(comments)
    except subprocess.TimeoutExpired:
        points -= 35.0
        comments.append('[-35] did not finish in 120s to run command: python3 Q2.SQL.py')
        return points, '; '.join(comments)

    points_per_section = 0
    points_per_section_code = 0
    final_output = []
    
    # parse Q2.OUT.txt
    submitted_output = parse_q2out_file(out_file_path)
    desired_output = [['parts   sets    themes'], ['1', '1', '1'], ['parts_index   sets_index    themes_index'], ['0,id,integer,0,,0', '1,name,text,0,,0'], ['count', '0b918943df0962bc7a1824c0555a389347b4febdc7cf9d1254406d80ce44e3f9'], ['theme,num_sets', '6e317bcd6839e8877395411b47b2b89d2bae7ccb05f78cee32bcdf76b5294265,8241649609f88ccd2a0a5b233a07a538ec313ff6adf695aa44a969dbca39f67d', '86ac6ab7840c79379d8770ff849017aad9020fed1812a62734660ed7f76824ab,c837649cce43f2729138e72cc315207057ac82599a59be72765a477f22d14a54', '6efced6a7e04d1137ae7e833b91a4b7660fc985091525eae5bf656819a7f31f9,0e17daca5f3e175f448bacace3bc0da47d0655a74c8dd0dc497a3afbdad95f1f', '1d2842862c1e5f87900e0b87b3efc8b6abf5d18899e254414649d55fe39f2d46,9f14025af0065b30e47e23ebb3b491d39ae8ed17d33739e5ff3827ffb3634953', '2d65828f5a6b97dd0dde7a95c9d32ba210a4f110a5068532923efc6d10f7088b,624b60c58c9d8bfb6ff1886c2fd605d2adeb6ea4da576068201b6c6958ce93f4', '057af45fb43ee158f7738eae864cde11b42b6ec6adf0df12d30e25fa32e34a92,670671cd97404156226e507973f2ab8330d3022ca96e0c93bdbdb320c41adcaf'], ['theme,percentage', '6e317bcd6839e8877395411b47b2b89d2bae7ccb05f78cee32bcdf76b5294265,de5ebb51c1398b41d5aad54105940c02eab78523158cbaa867e41d30ee3f776f', '86ac6ab7840c79379d8770ff849017aad9020fed1812a62734660ed7f76824ab,944bccb2c957f754a01120e3a7921213d4327b3c0070daa39a42035d8dae5c5e', '6efced6a7e04d1137ae7e833b91a4b7660fc985091525eae5bf656819a7f31f9,003514ce193fd40e19e381c8d8497eb8c5eb447e334a4873b677a17a58724865', '1d2842862c1e5f87900e0b87b3efc8b6abf5d18899e254414649d55fe39f2d46,de2eb6439cf3d842edb9eb123b56afb638e27ede347c86429389c554f0c41b1e', '2d65828f5a6b97dd0dde7a95c9d32ba210a4f110a5068532923efc6d10f7088b,ad5482cf6941dccd38150c2fe806cf771809d813996b683b2b44559bf39d136b', '057af45fb43ee158f7738eae864cde11b42b6ec6adf0df12d30e25fa32e34a92,16a29e295c5e00bc00f65e7485fd9388b550fc6e5ef22cb51e6ae1b62a3adfcd'], ['sub_theme,num_sets', '46d755b90f440bad11711d83be7588225cb14b13c3ea9500f0b4b82e3217a7ac,76a50887d8f1c2e9301755428990ad81479ee21c25b43215cf524541e0503269', '8f27f432fcbaa4b5180a1cc7a8fa166a93cda3c1bce6f19922dd519d02f4bb39,624b60c58c9d8bfb6ff1886c2fd605d2adeb6ea4da576068201b6c6958ce93f4', '26482652ab786704a80db8aecf46c550a8eda060e5cc94553928f4eb19d95bec,3fdba35f04dc8c462986c992bcf875546257113072a909c162f7e470e581e278', '1114f1eba77828092dc76651db61eb16133c7f3bd925ac6d58b72db538089a32,4fc82b26aecb47d2868c4efbe3581732a3e7cbcc6c2efb32062c08170a05eeb8', 'cfb7c605ff3839bf8b02cc6acc3565a16784f2776344f2f26f1ce14012d5c1f9,2c624232cdd221771294dfbb310aca000a0df6ac8b66b696d90ef06fdefb64a3', '0bf853b6a549dd69b531ca97ca0aefba2f0bacab31f7133673351e1af42d5689,7902699be42c8a8e46fbbb4501726517e86b22c56a189f7625a6da49081b2451', '0d1f28479f370677d597466bdf4aa4bd0ff847307a6e83e1cba2069155059af3,7902699be42c8a8e46fbbb4501726517e86b22c56a189f7625a6da49081b2451', '2cfbcfe05812153e072ff33134601bd5de930e376e08b988d3220d55412f40fb,e7f6c011776e8db7cd330b54174fd76f7d0216b612387a5ffcfb81e6f0919683', 'e0c799908ea9e185e80c0ea543ebcf0f31594a99f547ce0c47238b827e9c3697,e7f6c011776e8db7cd330b54174fd76f7d0216b612387a5ffcfb81e6f0919683'], ['0,rowid,integer,0,,0', '1,year,integer,0,,0', '2,sets_count,,0,,0', '0'], ['year,running_total', '1980,838f461c2fa673cec73e6eecdafa88b127802d6cb0a61c53175197a122cb645a', '1981,48b361d46638bfa4eee090c158a750a69c7beec3a62e703e2801125551b1b157', '1982,6b3c238ebcf1f3c07cf0e556faa82c6b8fe96840ff4b6b7e9962a2d855843a0b', '1983,814bb6b8dc12188a44b71e378dc20a4292e01979aa9ab95b09b8a681391dfc9d', '1984,549a2fac47d713cc00f2db498ad6b5574fb03c9293aef6c7ad50a11b394c197d', '1985,2c69bc9b34fb0800a44a702e45019c107dfdc8273b9feb62c9615addc7138bde', '1986,04edd1d7736883194af3ddb232c337e53d17bc93cfd2140c4f4c4e0d966798b1', '1987,7b81eb727ed48055fa55c5e03aaa43f27b01bd9b1c8eb38f37a1ca541a79c1f7', '1988,c22e1a4acbd2d996ff19a852585f9434883c30124f6b118eb9152fe4e5ee7994', '1989,e4c6a9f38e8e4d127290cf104ac1f46d0649c7db6c89f4bc10be7447bf1f514c'], ['0,part_num,,0,,0', '1,name,,0,,0', '2,part_cat_id,,0,,0', '3,part_material_id,,0,,0'], ['count_overview', '34f1a6ce1bbe867e1bb9b2f9574573354c4ef88ae6524aabbc5c9012a934b0c2'], ['total_boy_minidoll', '4fc82b26aecb47d2868c4efbe3581732a3e7cbcc6c2efb32062c08170a05eeb8'], ['total_girl_minidoll', 'bbb965ab0c80d6538cf2184babad2a564a010376712012bd07b0af92dcd3097d'], []]
    # alternate_f_output = parse_q2out_file(ALTERNATE_F_FILE_PATH)[0]

    # load Q2.db
    submitted_db_conn, submitted_db_cursor = load_q2db_file(db_file_path)
    desired_db_conn, desired_db_cursor = load_q2db_file(MODEL_DB_FILE_PATH)
    
    try:

        # if submitted_output == desired_output:
        #     return points, ''

        # test (a.i)
        if submitted_output[0] != desired_output[0]:
            if len(submitted_output[0]) < len(desired_output[0]):
                points -= 2.0
                points_per_section -= 2.0
                comments.append('(a.i) [-2] incorrect/no output')
            else:
                submitted_tables = submitted_output[0][0]

                if 'parts' not in submitted_tables:
                    points -= (2/3)
                    points_per_section -= (2/3)
                    comments.append('(a.i) [-1] parts table not found')

                if 'sets' not in submitted_tables:
                    points -= (2/3)
                    points_per_section -= (2/3)
                    comments.append('(a.i) [-1] sets table not found')

                if 'themes' not in submitted_tables:
                    points -= (2/3)
                    points_per_section -= (2/3)
                    comments.append('(a.i) [-1] themes table not found')

        final_output.append(points_per_section)
        points_per_section = 0
        
        # test (a.ii)
        if submitted_output[1] != desired_output[1]:
            submitted_tables = map(
                lambda t: str(t[0]),
                submitted_db_conn.execute(
                    'SELECT name from sqlite_master where type = \'table\';')
                .fetchall())

            if 'parts' not in submitted_tables:
                points -= 1.0
                points_per_section -= 1.0
                comments.append("(a.ii) [-1] no table 'parts'")
            if 'sets' not in submitted_tables:
                points -= 1.0
                points_per_section -= 1.0
                comments.append("(a.ii) [-1] no table 'sets'")
            if 'themes' not in submitted_tables:
                points -= 1.0
                points_per_section -= 1.0
                comments.append("(a.ii) [-1] no table 'themes'")  
            if 'parts' in submitted_tables:
                if len(submitted_output[1]) < len(desired_output[1]):
                    points -= 1.0
                    points_per_section -= 1.0
                    comments.append('(a.ii) [-1] incorrect/no output')
                else:

                    desired_count_parts = desired_output[1][0]
                    submitted_count_parts = submitted_output[1][0]
                    if submitted_count_parts != desired_count_parts:
                        points -= 0.33
                        points_per_section -= 0.33
                        comments.append('(a.ii) [-0.33] wrong number of items in parts table or table does not exist')

            if 'sets' in submitted_tables:
                if len(submitted_output[1]) < len(desired_output[1]):
                    points -= 1.0
                    points_per_section -= 1.0
                    comments.append('(a.ii) [-1] incorrect/no output')
                else:

                    desired_count_sets = desired_output[1][1]
                    submitted_count_sets = submitted_output[1][1]
                    if submitted_count_sets != desired_count_sets:
                        points -= 0.33
                        points_per_section -= 0.33
                        comments.append('(a.ii) [-0.33] wrong number of items in sets table or table does not exist')
            
            if 'themes' in submitted_tables:
                if len(submitted_output[1]) < len(desired_output[1]):
                    points -= 1.0
                    points_per_section -= 1.0
                    comments.append('(a.ii) [-1] incorrect/no output')
                else:

                    desired_count_theme = desired_output[1][2]
                    submitted_count_theme = submitted_output[1][2]
                    if submitted_count_theme != desired_count_theme:
                        points -= 0.34
                        points_per_section -= 0.34
                        comments.append('(a.ii) [-0.33] wrong number of items in themes table or table does not exist')

        final_output.append(points_per_section)
        points_per_section = 0

        # test (b)
        if submitted_output[2] != desired_output[2]:
            if len(submitted_output[2]) < len(desired_output[2]):
                points -= 3.0
                points_per_section -= 3.0
                comments.append('(b) [-3] incorrect/no output')
            else:
                desired_indexes = desired_output[2][0].split()
                submitted_indexes = submitted_output[2][0].split()
                not_found = list()
                for index in desired_indexes:
                    if index in submitted_indexes:
                        continue
                    else:
                        not_found.append(index)

                if len(not_found) > 0:
                    deducted = 1 * len(not_found)
                    comments.append('(b) [-{}] index not found: {}'.format(
                        deducted,
                        ', '.join(not_found)
                    ))
                    points -= deducted
                    points_per_section -= deducted
        
        final_output.append(points_per_section)
        points_per_section = 0
        
        # test (c.i)
        if True:
            query = 'SELECT * FROM top_level_themes;'
            query_check = "SELECT count(*) FROM sqlite_master WHERE type='table' AND name='top_level_themes';"
            if([str(t) for t in submitted_db_conn.execute(query_check).fetchall()][0][1] == '0'):
                submitted_toplevel = [str(t) for t in submitted_db_conn.execute(query).fetchall()]
                desired_toplevel = [str(t) for t in desired_db_conn.execute(query).fetchall()]

                true_positive = 0
                for toplevel in desired_toplevel:
                    if toplevel in submitted_toplevel:
                        true_positive += 1

                false_positive = 0
                for toplevel in submitted_toplevel:
                    if toplevel not in desired_toplevel:
                        false_positive += 1

                if false_positive > true_positive:
                    points -= 2.0
                    points_per_section -= 2.0
                    comments.append('(c.i) [-2] incorrect/no output')
                elif true_positive < len(desired_toplevel) or false_positive > 0:
                    points -= 1.0
                    points_per_section -= 1.0
                    comments.append('(c.i) [-1] partially incorrect output')

                del submitted_toplevel
                del desired_toplevel
            else:
                points -= 2.0
                points_per_section -= 2.0
                comments.append('(c.i) [-2] table not found')
        final_output.append(points_per_section)
        points_per_section = 0

        # test (c.ii)
        if hashlib.sha256(submitted_output[4][1].encode()).hexdigest() != desired_output[4][1] or submitted_output[4][0] != desired_output[4][0]:
            if(len(submitted_output[4]) > 0):
                if submitted_output[4][1] != submitted_output[4][1]:
                    points -= 1.0
                    points_per_section -= 1.0
                    comments.append('(c.ii) [-1] correct count but incorrect column name')
                else:
                    points -= 2.0
                    points_per_section -= 2.0
                    comments.append('(c.ii) [-2] incorrect/no output')
            else:
                points -= 2.0
                points_per_section -= 2.0
                comments.append('(c.ii) [-2] incorrect/no output') 
        final_output.append(points_per_section)
        points_per_section = 0

        # test (d)
        submitted_output_new = []
        submitted_output_new.append('theme,num_sets')
        for i in range(len(submitted_output[5])-1):
            submitted_output_new.append(str(hashlib.sha256(submitted_output[5][i+1].split(",")[0].encode()).hexdigest()) + "," + str(hashlib.sha256(submitted_output[5][i+1].split(",")[1].encode()).hexdigest()))

        if submitted_output_new != desired_output[5]:
            part_points = 0
            part_comments = list()

            try:
                test_d_data = submitted_output_new[0]
            except IndexError:
                test_d_data = None

            if test_d_data is not None:
                if submitted_output_new[0] == desired_output[5][0]:
                    part_points += 0.5
                    part_comments.append('correct format')

            if len(submitted_output_new) > len(desired_output[5]):
                num_present = 0
                desired_len = len(desired_output[5]) - 1
                for entry in desired_output[5][1:]:
                    if entry in submitted_output_new:
                        num_present += 1

                if num_present == desired_len:
                    part_points += 1.5
                    part_comments.append('more than {} entries, but required entries are present'.format(
                        desired_len
                    ))
            elif len(submitted_output[5]) == len(desired_output[5]):
                part_points += 1.0
                part_comments.append('correct number of entries but incorrect entries/order of entries')
            else:
                part_comments.append('incorrect/no output')

            deduction = 4 - part_points
            points -= deduction
            points_per_section -= deduction
            comments.append('(d) [-{}] {}'.format(deduction, ', '.join(part_comments)))

        final_output.append(points_per_section)
        points_per_section = 0 

        # test (e)
        
        submitted_output_new = []
        submitted_output_new.append('theme,percentage')
        for i in range(len(submitted_output[6])-1):
            submitted_output_new.append(str(hashlib.sha256(submitted_output[6][i+1].split(",")[0].encode()).hexdigest()) + "," + str(hashlib.sha256(submitted_output[6][i+1].split(",")[1].encode()).hexdigest()))
        desired_output_new = ['theme,percentage', 
'6e317bcd6839e8877395411b47b2b89d2bae7ccb05f78cee32bcdf76b5294265,de5ebb51c1398b41d5aad54105940c02eab78523158cbaa867e41d30ee3f776f', 
'86ac6ab7840c79379d8770ff849017aad9020fed1812a62734660ed7f76824ab,944bccb2c957f754a01120e3a7921213d4327b3c0070daa39a42035d8dae5c5e', 
'6efced6a7e04d1137ae7e833b91a4b7660fc985091525eae5bf656819a7f31f9,e0b04046fbfbc96f3437e4718a8a15e7eb5936298a36a8c2039226d1c5f41845', 
'1d2842862c1e5f87900e0b87b3efc8b6abf5d18899e254414649d55fe39f2d46,de2eb6439cf3d842edb9eb123b56afb638e27ede347c86429389c554f0c41b1e', 
'2d65828f5a6b97dd0dde7a95c9d32ba210a4f110a5068532923efc6d10f7088b,ad5482cf6941dccd38150c2fe806cf771809d813996b683b2b44559bf39d136b', 
'057af45fb43ee158f7738eae864cde11b42b6ec6adf0df12d30e25fa32e34a92,16a29e295c5e00bc00f65e7485fd9388b550fc6e5ef22cb51e6ae1b62a3adfcd']
        if submitted_output_new != desired_output[6] and submitted_output_new != desired_output_new:
            part_points = 0
            part_comments = list()

            try:
                test_e_data = submitted_output[6][0]
            except IndexError:
                test_e_data = None

            if test_e_data is not None:
                if submitted_output_new[0] == desired_output[6][0]:
                    part_points += 0.5
                    part_comments.append('correct format')

            if len(submitted_output_new) > len(desired_output[6]):
                num_present = 0
                desired_len = len(desired_output[6]) - 1
                for entry in desired_output[6][1:]:
                    if entry in submitted_output_new[1:]:
                        num_present += 1

                if num_present == desired_len:
                    part_points += 5.5
                    part_comments.append('more than {} entries, but required entries are present'.format(
                        desired_len
                    ))
            elif len(submitted_output[6]) == len(desired_output[6]):
                part_points += 1.0
                part_comments.append('correct number of entries but incorrect entries/order of entries')
            else:
                part_comments.append('incorrect/no output')

            deduction = 7 - part_points
            points -= deduction
            points_per_section -= deduction
            comments.append('(e) [-{}] {}'.format(deduction, ', '.join(part_comments)))
        
        final_output.append(points_per_section)
        points_per_section = 0

        # test (f)
        submitted_output_new = []
        submitted_output_new.append('sub_theme,num_sets')
        for i in range(len(submitted_output[7])-1):
            submitted_output_new.append(str(hashlib.sha256(submitted_output[7][i+1].split(",")[0].encode()).hexdigest()) + "," + str(hashlib.sha256(submitted_output[7][i+1].split(",")[1].encode()).hexdigest()))
    
        if submitted_output_new != desired_output[7]:
            not_found = list()
            found = list()
            part_comments = list()
            deduction = 0.0
            
            subtheme_counts = {k: v for k, v in (s.split(',') for s in desired_output[7][1:])}
            subtheme_names = list(subtheme_counts.keys())
            try:
                submitted_counts = {k: v for k, v in (s.split(',') for s in submitted_output_new[1:])}
            except:
                deduction += 4.0
                part_comments.append('incorrect format')
            else:
                submitted_themes = list(submitted_counts.keys())
                
                for subtheme in subtheme_names:
                    for submitted_subtheme in submitted_themes:
                        if hashlib.sha256(submitted_subtheme.encode()).hexdigest() == subtheme:
                            found.append(subtheme)
                            break
                    else:
                        not_found.append(subtheme)
                
                if len(not_found) > 0:
                    deduction += (float(len(not_found) / len(subtheme_names))) * 2.0
                    part_comments.append('missing subthemes {}'.format(', '.join('"' + s + '"' for s in not_found)))
                
                incorrect = 0
                for k, v in subtheme_counts.items():
                    if k in found:
                        try:
                            if int(v) == int(submitted_counts[k]):
                                continue
                            else:
                                incorrect += 1
                        except:
                            incorrect += 1
                    else:
                        incorrect += 1
                
                if incorrect > 0:
                    deduction += (float(incorrect / len(subtheme_names))) * 2.0
                    part_comments.append('{} incorrect or missing count values'.format(incorrect))
            
            if deduction > 0.0:
                points -= deduction
                points_per_section -= deduction
                comments.append('(f) [-{:0.4g}] {}'.format(deduction, ', '.join(part_comments)))
        
        final_output.append(points_per_section)
        points_per_section = 0

        # test (g.i)
        if (submitted_output[8][:-1] != desired_output[8][:-1]): 
            
            not_found = list()
            columns = ['rowid', 'year', 'sets_count']
            for column in columns:
                for column_info in submitted_output[8][:-1]:
                    if column in column_info:
                        break
                else:
                    not_found.append(column)
            
            if len(not_found) > 0:
                deduction = (float(len(not_found)) / len(columns)) * 2.0
                points -= deduction
                points_per_section -= deduction
                comments.append('(g.i) [-{:0.4g}] view columns not found: {}'.format(deduction, ', '.join(not_found)))
        
        final_output.append(points_per_section)
        points_per_section = 0

        # test (g.ii)
        submitted_output_new = []
        submitted_output_new.append('year,running_total')
        for i in range(len(submitted_output[9])-1):
            submitted_output_new.append(str(submitted_output[9][i+1].split(",")[0]) + "," + str(hashlib.sha256(submitted_output[9][i+1].split(",")[1].encode()).hexdigest())) 
        
        if submitted_output_new != desired_output[9]:
            part_points = 0
            part_comments = list()

            try:
                test_gii_data = submitted_output_new[0]
            except IndexError:
                test_gii_data = None

            if test_gii_data is not None:
                if submitted_output_new[0] == desired_output[9][0]:
                    part_points += 0.5
                    part_comments.append('correct format')
            
            submitted_unordered = {y: v for y, v in [s.split(',') for s in submitted_output_new[1:][::-1]]}
            desired_unordered = {y: v for y, v in [s.split(',') for s in desired_output[9][1:][::-1]]}
            if submitted_unordered == desired_unordered:
                part_points += 2.0
                part_comments.append('correct values, but not ordered ascending by year')
            elif len(submitted_output_new) > 0:
                part_points += 1.0
                part_comments.append('incorrect output')
            else:
                part_comments.append('incorrect/no output')

            deduction = 4 - part_points
            points -= deduction
            points_per_section -= deduction
            comments.append('(g.ii) [-{}] {}'.format(deduction, ', '.join(part_comments)))

        final_output.append(points_per_section)
        points_per_section = 0

        # test (h.i)
        try:
            if hashlib.sha256(submitted_output[11][1].encode()).hexdigest() != desired_output[11][1] or submitted_output[11][0] != desired_output[11][0]:
                points -= 1.0
                points_per_section -= 1.0
                comments.append('(h.i) [-1] incorrect/no output')
        except IndexError:
            points -= 1.0
            points_per_section -= 1.0
            comments.append('(h.i) [-1] incorrect/no output')

        final_output.append(points_per_section)
        points_per_section = 0

        # test h.ii
        try:
            if hashlib.sha256(submitted_output[12][1].encode()).hexdigest() != desired_output[12][1] or submitted_output[12][0] != desired_output[12][0]:
                points -= 1.0
                points_per_section -= 1.0
                comments.append('(h.ii) [-1] incorrect/no output')
        except IndexError:
            points -= 1.0
            points_per_section -= 1.0
            comments.append('(h.ii) [-1] incorrect/no output')
        final_output.append(points_per_section)
        points_per_section = 0

        # test h.iii
        try:
            if hashlib.sha256(submitted_output[13][1].encode()).hexdigest() != desired_output[13][1] or submitted_output[13][0] != desired_output[13][0]:
                points -= 1.0
                points_per_section -= 1.0
                comments.append('(h.iii) [-1] incorrect/no output')
        except IndexError:
            points -= 1.0
            points_per_section -= 1.0
            comments.append('(h.iii) [-1] incorrect/no output')
        final_output.append(points_per_section)
        final_output.append(points_per_section_code)

        if points == 35.0 and len(comments) == 0:
            comments.append('good job!')
        elif points == 35.0 and len(comments) != 0:
            raise Exception('Error in autograder, full points awarded, but comments added')
        elif points != 35.0 and len(comments) == 0:
            raise Exception('Error in autograder, points were deducted, but no comments added')
    finally:
        # teardown
        submitted_db_conn.close()
        desired_db_conn.close()
    
      
    return max(0.0, points), str(final_output).strip('[]') + ","+ '; '.join(comments)



if __name__ == '__main__':
    headers = ['Total Score: ','Part a(i): ','Part a(ii): ','Part b: ','Part c(i): ','Part c(ii): ','Part d: ','Part e: ','Part f: ','Part g(i): ','Part g(ii): ','Part h(i): ','Part h(ii): ','Part h(iii): ','Alterations: ','Final Comment: ']
    score = evaluate()
    score_split=score[1].split(',')
    for i in range(15):
        print(headers[i+1]+score_split[i])
    print (headers[0] + str(score[0]))
