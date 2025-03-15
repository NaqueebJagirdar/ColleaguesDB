# add_colleagues.py
from myapp.__main__ import app, db, Colleague

def add_colleagues():
    with app.app_context():
        colleagues = [
            # WSE Experts / Assistance / WSE-01 (GER) etc. were omitted as requested
            Colleague(name="Christoph Hilling"),
            Colleague(name="Héctor Rodríguez"),
            Colleague(name="Birthe Kaiser"),
            Colleague(name="Claudia Meinherz"),
            Colleague(name="Daniela Redenius"),
            Colleague(name="Rafaela Penning"),
            Colleague(name="Martin Hegermann"),
            Colleague(name="Katharina Hiepko"),
            Colleague(name="Tobias Kapschefsky"),
            Colleague(name="Uta Zwölfer-Dorau"),
            Colleague(name="Maria Böhme"),
            Colleague(name="Sarah Freund"),
            Colleague(name="Stephan Hohmann"),
            Colleague(name="Till Grünewald"),
            Colleague(name="Derya Mohr"),
            Colleague(name="Anil Dardagan"),
            Colleague(name="Christian Züwerink"),

            # WSE-02 (AM) omitted as requested
            Colleague(name="Alysson Sehn"),
            Colleague(name="Ana Kelly Monte"),
            Colleague(name="Andrei Santos"),
            Colleague(name="Antonio Carvalho"),
            Colleague(name="Bernardo Gomes"),
            Colleague(name="Carlos Pinto"),
            Colleague(name="Chrystel Alzin"),
            Colleague(name="Elaíne Oliveira"),
            Colleague(name="Gustavo Costa"),
            Colleague(name="Júlia Brzuska"),
            Colleague(name="Max Maruyama"),
            Colleague(name="Rafael Batista"),
            Colleague(name="Rodrigo Vieira"),
            Colleague(name="Sami Chebil"),
            Colleague(name="Vanessa Silva"),

            # WSE-03 (SEA) omitted as requested
            Colleague(name="Beatrice Pistoni"),
            Colleague(name="Cristoffer Fernandes"),
            Colleague(name="Ricardo Rocha"),
            Colleague(name="Funda Uz"),
            Colleague(name="Ahmet Kocaturk"),
            Colleague(name="Ozgun Ozis"),
            Colleague(name="Ioannis Barkoutsos"),
            Colleague(name="Yusuf Sair"),
            Colleague(name="Giovanni Tozzi"),
            Colleague(name="Jesus Monteiro"),
            Colleague(name="Diogo Miguel"),

            # WSE-04 (CN&WE) omitted as requested
            Colleague(name="Antoine Rochet"),
            Colleague(name="Marc Jandl"),
            Colleague(name="Nico Braun"),
            Colleague(name="Paul Ladstätter"),
            Colleague(name="Callum Bell"),
            Colleague(name="Maurizio Bracalente"),
            Colleague(name="Guillermo (Bautista) Fernandez"),
            Colleague(name="Ulrike Spörl"),
            Colleague(name="Christian Rösner"),

            # WSE-05 (APAC) omitted as requested
            Colleague(name="Robert Lai"),
            Colleague(name="Fernando Cruz"),
            Colleague(name="Sudhakar"),
            Colleague(name="Ramesh Moorthy"),
            Colleague(name="Nethaji Radhakrishnan"),
            Colleague(name="Jeyamurugan JM"),
            Colleague(name="Mohammad Imran"),
            Colleague(name="Abhin Ananthakrishnan"),
            Colleague(name="Hudson Samraj A"),
            Colleague(name="Saravana Kumar P"),
            Colleague(name="Mohd Jagirdar"),
            Colleague(name="Senthilkumar N"),
            Colleague(name="Trinh Tung Lam"),
            Colleague(name="Tran Anh Tuan"),

            # WSE-06 (NC) omitted as requested
            Colleague(name="Cordula Hornung"),
            Colleague(name="Alexander Weiß"),
            Colleague(name="Christian Meckenhäuser"),
            Colleague(name="Christian Wiedenhöft"),
            Colleague(name="Eric Merfels"),
            Colleague(name="Henriette Labsch"),
            Colleague(name="Moritz Kausche"),
            Colleague(name="Peter Ihly"),
            Colleague(name="Silke Peters"),

            # CRQ omitted as requested
            Colleague(name="Sönke Bemmann"),
            Colleague(name="Olmo Duran")
        ]

        # Add all colleagues to the session
        db.session.add_all(colleagues)

        # Commit the transaction
        db.session.commit()
        print("All colleagues added successfully!")


if __name__ == "__main__":
    add_colleagues()
