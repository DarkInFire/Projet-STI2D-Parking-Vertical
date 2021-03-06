#define NBCodes 30
#define DelaiEnvoie 38
#define PinCommande 8

int PlacesActives[15]={1,1,1,1,1,1,1,1,1,1,1,1,1,1,1}; // 1: active | 0: non active
int PlacesDispos[15]={1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};  // 1: disponible | 0: non disponible
int PlacesPredef[15]={0,0,0,0,0,0,0,0,0,0,0,0,0,0,0}; // 1: predefinie | 0: non predefinie
char PlacesCodes[15][11]={"0000000000","0000000000","0000000000","0000000000","0000000000","0000000000","0000000000","0000000000","0000000000","0000000000","0000000000","0000000000","0000000000","0000000000","0000000000"}; // code attribuer a chaques places | 0000000000: aucun code
int PlaceDuCode_PlacesCodes = 1000;

int Etat_Parking = 1; // 1: parking actif | 0: parking desactive

int PlacesParking[15]={31,41,51,33,34,35,43,32,54,53,52,44,45,55,42};

char CodeAutoriser[NBCodes][11];
int NombreCodes = 0;
int PlaceDuCode_CodeAutoriser = 1000;

void setup() {
  Serial.begin(9600);
  Serial.print("NoRaj de mon Arduinaj !");
  pinMode(PinCommande, OUTPUT);
}


void loop() {
  
  int donneesALire = Serial.available(); //lecture du nombre de caractères disponibles dans le buffer
  if(donneesALire > 0) { //si le buffer n'est pas vide
  
    /*
    a0000000000   ajoute un badge
    b0000000000   supprime un badge
    c0000000000   utilisateur arrive
    d             stats          
    e             badges
    f000000000011 associe un badge a une place    
    */
    
    char Commande = Serial.read();
    if (Commande=='a') {
      String TempCode;
      char Code[11];
      TempCode = Serial.readStringUntil('\n');
      TempCode.toCharArray(Code, 11) ;
      if (TempCode.length()==10) {
        AjouteCodeAutorise(Code);
      }
    } else if (Commande=='b') {
      String TempCode;
      char Code[11];
      TempCode = Serial.readStringUntil('\n');
      TempCode.toCharArray(Code, 11) ;
      if (TempCode.length()==10) {
        SupprimeCodeAutorise(Code);
      }
    } else if (Commande=='c') {
      String TempCode;
      char Code[11];
      TempCode = Serial.readStringUntil('\n');
      TempCode.toCharArray(Code, 11) ;
      if (TempCode.length()==10) {
        CodeDetecte(Code);
      }
    } else if (Commande=='d') {
      int b = 0;
      for(int a = 0;a<15;a++) {
        if(PlacesDispos[a]==1) {
          b++;
        }
      }
      Serial.print("\nIl y a ");
      Serial.print(NombreCodes);
      Serial.print(" code");
      Serial.print("\nIl y a ");
      Serial.print(b);
      Serial.print(" places disponibles");
    } else if (Commande=='e') {
      for(int a = 0;a<15;a++) {
        Serial.print("\n");
        Serial.print(a);
        Serial.print(" -> ");
        Serial.print(PlacesCodes[a]);
      }
    } else if (Commande=='f') {
      String TempCode;
      char Code[10];
      char plac[2];
      TempCode = Serial.readStringUntil('\n');
      //TempCode.toCharArray(Code, 12) ;
      for(int a = 0;a<10;a++) {
        Code[a] = TempCode[a];
      }
      Code[10] = '\0';
      for(int a = 10;a<12;a++) {
        plac[a-10] = TempCode[a];
      }
      plac[2] = '\0';
      Serial.print("\nLe code ");
      Serial.print(Code);
      Serial.print(" a ete associe a la place ");
      Serial.print(plac);
      AjouteCodeAutorise(Code);
      PlacesPredef[atoi(plac)] = 1;
      strcpy(PlacesCodes[atoi(plac)], Code);
    }
    
  }
  
}


/*
---------------------------------------------------------------------------
GESTION CODES AUTORISE
---------------------------------------------------------------------------
*/
void AjouteCodeAutorise(char code[10]) { // ajoute un code au tableau CodeAutoriser
  if (VerifieCodeAutorise(code)==1000) {
    for(int a = 0;a<10;a++) {
      CodeAutoriser[NombreCodes][a] = code[a];
    }
    NombreCodes++;
    Serial.print("\nLe code : ");
    Serial.print(code);
    Serial.print(" a ete ajoute");
  }
}

void SupprimeCodeAutorise(char code[10]) { // supprime un code du tableau CodeAutoriser et remet en forme
  if (VerifieCodeAutorise(code)!=1000) {
    for(int a = VerifieCodeAutorise(code);a<NombreCodes;a++) {   
      for(int b = 0;b<10;b++) {
        CodeAutoriser[a][b] = code[b];
      }
    }
    for(int a = 0;a<10;a++) {
      CodeAutoriser[NombreCodes][a] = '\0';
    }
    NombreCodes--;
    Serial.print("\nLe code : ");
    Serial.print(code);
    Serial.print(" a ete supprime");
  }
}

int VerifieCodeAutorise(char code[10]) { // verifie si code existe et retourne son emplacement dans le tableau CodeAutoriser
  PlaceDuCode_CodeAutoriser = 1000;
  for(int a = 0;a<NombreCodes;a++) {
    if (strcmp(CodeAutoriser[a], code)==0) {
      PlaceDuCode_CodeAutoriser = a;
    }
  }
  return PlaceDuCode_CodeAutoriser;
}

/*
---------------------------------------------------------------------------
GESTION PARKING
---------------------------------------------------------------------------
*/
void CodeDetecte(char code[10]) {
  if (VerifieCodeAutorise(code)!=1000) {
    if (VerifieCodeParking(code)!=1000) { // voiture sortante ou place predef
      if (PlacesPredef[VerifieCodeParking(code)]==1) { // place predef
        if (PlacesDispos[VerifieCodeParking(code)]==1) { // voiture place predef entrante
          PlacesDispos[VerifieCodeParking(code)] = 0;
          EnvoieCommande(VerifieCodeParking(code));
          // ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        } else { // voiture place predef sortante
          PlacesDispos[VerifieCodeParking(code)] = 1;
          EnvoieCommande(VerifieCodeParking(code));
          // ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        }
      } else { // voiture sortante 
        Serial.print("\nLa place : ");
        Serial.print(VerifieCodeParking(code));
        Serial.print(" a ete decharger avec le code : ");
        Serial.print(code);
        // ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        PlacesDispos[VerifieCodeParking(code)] = 1;
        EnvoieCommande(VerifieCodeParking(code));
        SupprimeCodeParking(VerifieCodeParking(code));
      }
    } else { // voiture entrante
      for(int a = 0;a<15;a++) { // cherche une place
        if(PlacesPredef[a]==0 && PlacesDispos[a]==1 && PlacesActives[a]==1) { // place trouvee
          EnvoieCommande(a);
          PlacesDispos[a] = 0;
          AjouteCodeParking(code, a);
          // ----------------------------------------------------------------------------------------------------------------------------------------------------------------
          Serial.print("\nLa place : ");
          Serial.print(a);
          Serial.print(" a ete charger avec le code : ");
          Serial.print(code);
          a = 15;
        }
      }
    }
  } else { // code non valide
  Serial.print("\nLe code : ");
  Serial.print(code);
  Serial.print(" est invalide");
  // ----------------------------------------------------------------------------------------------------------------------------------------------------------------
  }
}

void EnvoieCommande(int place) {
  Serial.print("\nEnvoie de : ");
  Serial.print(PlacesParking[place]);
  Serial.print(" impulsions");
  for(int a = 0;a<PlacesParking[place];a++) {
    delay(DelaiEnvoie);
    digitalWrite(PinCommande, HIGH);
    delay(DelaiEnvoie);
    digitalWrite(PinCommande, LOW);
  }
}

void AjouteCodeParking(char code[10], int place) { // ajoute un code au tableau PlacesCodes
  for(int a = 0;a<10;a++) {
    PlacesCodes[place][a] = code[a];
  }
}

void SupprimeCodeParking(int place) { // supprime un code du tableau PlacesCodes
  for(int a = 0;a<10;a++) {
    PlacesCodes[place][a] = '0';
  }
}

int VerifieCodeParking(char code[10]) { // verifie si code existe et retourne son emplacement dans le tableau PlacesCodes
  PlaceDuCode_PlacesCodes = 1000;
  for(int a = 0;a<15;a++) {
    if (strcmp(PlacesCodes[a], code)==0) {
      PlaceDuCode_PlacesCodes = a;
    }
  }
  return PlaceDuCode_PlacesCodes;
}
