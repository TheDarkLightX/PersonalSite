import ReleaseDesk

/-! Executable projection of the *same* step definition used in the proofs.
This replay is an exhaustive test, not a theorem about the Rust compiler. -/

open ReleaseDesk

def statusCode : Status → Nat
  | .pending => 150 | .approved => 151 | .cancelled => 152
def officerCode : Officer → Nat
  | .nobody => 160 | .alice => 161 | .bob => 162 | .carol => 163
def commandCode : Command → Nat
  | .approve => 140 | .cancel => 141
def className : Class → String
  | .accept => "Accept" | .reject => "Reject"
  | .failure => "CommittedFailure" | .refused => "refused"

#eval do
  let officers : List Officer := [.nobody, .alice, .bob, .carol]
  for status in [Status.pending, .approved, .cancelled] do
    for first in officers do
      for second in officers do
        for command in [Command.approve, .cancel] do
          for officer in officers do
            let d := step ⟨status, first, second⟩ command officer
            IO.println s!"{statusCode status} {officerCode first} {officerCode second} {commandCode command} {officerCode officer} | {className d.kind} {statusCode d.next.status} {officerCode d.next.first} {officerCode d.next.second} {d.releases}"
